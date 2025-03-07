"""Module die alle functies die nodig zijn om de snelste route te vinden langs alle peilbuizen gegroepeerd per project."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/00_main.ipynb.

# %% auto 0
__all__ = ['project_root', 'use_pickle', 'df_grouped', 'RouteCreationError', 'create_group_route', 'process_peilbuizen_routes']

# %% ../../nbs/00_main.ipynb 4
import yaml
import pandas as pd
import logging
from datetime import datetime
from fastcore.utils import Path
from tqdm import tqdm

from .data_get import get_data_from_azuresql, load_pickle
from .route_get import create_optimized_route
from .data_export import get_waypoint_coords, convert_routejson_to_df, create_route_prev_next, google_maps_route_url
from .utils import get_project_root, make_filesystem_friendly, save_route_url, setup_logging

# %% ../../nbs/00_main.ipynb 7
class RouteCreationError(Exception):
    """Exception raised when a route cannot be created."""
    pass

# %% ../../nbs/00_main.ipynb 9
project_root = get_project_root()

with open(project_root / 'settings.yaml', 'r') as f:
    settings = yaml.safe_load(f)

# %% ../../nbs/00_main.ipynb 11
use_pickle=settings['files']['use_pickle_input']

if use_pickle:
    peilbuizen_df = load_pickle(settings['files']['pickle_file_input'])
else:
    peilbuizen_df = get_data_from_azuresql(sql_statement=settings['sql_statement']['peilbuizen'], 
                                       save_to_pickle=settings['files']['save_to_pickle'])

df_grouped = peilbuizen_df.groupby('project')

# %% ../../nbs/00_main.ipynb 17
def create_group_route(start_address: str, # De startlocatie en eindlocatie opgegeven als adres
                       group_df: pd.DataFrame, # De pandas dataframe met peilbuizen in de groep, bijv. op basis van project
                       route_profile: str, # Het route profiel (transport methode) waarvoor de route berekend moet worden
                       project_name: str, # Naam van de groep, bijv. Project Vecht
                       output_dir: str = 'output', # Locatie waar de resultaten en log-file opgeslagen worden. Als niks wordt opgegeven komen de resultaten in de output folder.
                       current_date: str = None, # De datum. Als niks wordt opgegeven, wordt de huidige datum gebruikt.
                       ) -> None:
    """
    Create optimized route for a group and save results
    """
    if current_date is None:
        current_date = datetime.now().strftime('%Y-%m-%d')
        
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        # Get optimized route
        route_json = create_optimized_route(start_address, group_df, route_profile)
        route_coords = get_waypoint_coords(route_json)
        
        # Create route dataframe
        optimized_route = convert_routejson_to_df(route_coords, group_df)
        route_table = create_route_prev_next(optimized_route)
        
        # Create filenames
        safe_project_name = make_filesystem_friendly(project_name)
        base_filename = f"peilbuizenroute_{safe_project_name}_{current_date}"
        
        # Save Excel file
        excel_path = output_path / f"{base_filename}.xlsx"
        route_table.to_excel(excel_path)
        
        # Save URL shortcut
        url = google_maps_route_url(route_coords)
        save_route_url(url, output_dir, f"{base_filename}.url")
        
    except Exception as e:
        raise RouteCreationError(f"Error processing group {project_name}: {str(e)}") from e


# %% ../../nbs/00_main.ipynb 19
def process_peilbuizen_routes(df: pd.DataFrame, # Dataframe van alle peilbuis groepen waarvoor route berekend wordt
                            start_address: str, # De startlocatie en eindlocatie opgegeven als adres
                            route_profile: str, # De route profiel (transport methode) waarvoor de route berekend moet worden
                            output_dir: str = 'output' # Locatie waar de resultaten en log-file opgeslagen worden. Als niks wordt opgegeven komen de resultaten in de output folder.
                            ) -> None:
    """
    Process peilbuizen dataframe, create optimized routes for each group,
    and save results to Excel and URL files
    
    Args:
        df: DataFrame with peilbuizen data
        start_address: Starting location address
        route_profile: De route profiel (transport methode) waarvoor de route berekend moet worden
        output_dir: Directory to save output files
    """
    # Create output directory and setup logging
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    current_date = datetime.now().strftime('%Y-%m-%d')
    logger = setup_logging(output_dir, current_date)
        
    # Process each group
    grouped = df.groupby('project')
    total_groups = len(grouped)
    
    for project_name, group_df in tqdm(grouped, total=total_groups,desc="Processing peilbuis routes per project."):
        if len(group_df) < 4:
            msg = f"Project {project_name} heeft 3 of minder locaties. Optimale route uitrekenen is zinloos."
            print(msg)
            logger.info(msg)
        elif len(group_df) > 70:
            msg = f"Project {project_name} heeft meer dan 70 locaties. Optimale route uitrekenen is niet mogelijk op de publieke Openrouteservice. Oplossing: verdeel het project in kleinere delen, zet de Openrouteservice op eigen omgeving."
            print(msg)
            logger.info(msg)
        else:
            #TODO: Als deze functie een error returned, dus geen route vindt, komt dat niet in logfiles.
            try:
                create_group_route(
                    start_address=start_address,
                    group_df=group_df,
                    route_profile=route_profile,
                    project_name=project_name,
                    output_dir=output_dir,
                    current_date=current_date
                )
                logger.info(f"Successfully processed route for project: {project_name}")
            except RouteCreationError as e:
                error_msg = str(e)
                print(error_msg)
                logger.error(error_msg)
            except Exception as e:
                error_msg = f"Error processing project {project_name}: {str(e)}"
                print(error_msg)
                logger.error(error_msg)

# %% ../../nbs/00_main.ipynb 21
#| eval: false
# eval set to false, else it will run the code for all projects everytime an nbdev_prepare is run.

process_peilbuizen_routes(df=peilbuizen_df,
                          start_address=settings['calculation']['startlocation'],
                          route_profile=settings['calculation']['distance_calculation_method'],
                          utput_dir=settings['files']['path_results'])
