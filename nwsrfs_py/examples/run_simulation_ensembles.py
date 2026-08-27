from nwsrfs_py import simulation
import os
import shutil
import tqdm
import numpy as np
import pandas as pd

DATA_DIR = "/Users/elischwat/Development/data/nwrfc-westwrf"
TARGET_DIR = "/Users/elischwat/Development/nwsrfs-hydro-models/nwsrfs_py/nwsrfs_py/data/HHDW1"
ARCHIVE_DIR = "/Users/elischwat/Development/data/nwrfc-westwrf/HHDW1_archive"

def main():
    print("Initializing NWSRFS Simulation Example...")
    print(" ")

    source_parent_directory = os.path.join(DATA_DIR, "HHDW1/ensemble_forcings")

    mefp_ensemble_names = os.listdir(os.path.join(source_parent_directory, "mefp"))
    mefp_ensemble_names = [f for f in mefp_ensemble_names if not f.startswith('.')]
    mefp_keys_and_paths = [
        (f"mefp_{mefp_ensemble}", os.path.join(source_parent_directory, "mefp", mefp_ensemble))
        for mefp_ensemble in mefp_ensemble_names
    ]
    
    westwrf_ensemble_names = os.listdir(os.path.join(source_parent_directory, "westwrf"))
    westwrf_ensemble_names = [f for f in westwrf_ensemble_names if not f.startswith('.')]
    westwrf_keys_and_paths = [
        (f"westwrf_{westwrf_ensemble}", os.path.join(source_parent_directory, "westwrf", westwrf_ensemble))
        for westwrf_ensemble in westwrf_ensemble_names
    ]

    aorc_ensemble_names = os.listdir(os.path.join(source_parent_directory, "aorc"))
    aorc_ensemble_names = [f for f in aorc_ensemble_names if not f.startswith('.')]
    aorc_keys_and_paths = [
        (f"aorc_{aorc_ensemble}", os.path.join(source_parent_directory, "aorc", aorc_ensemble))
        for aorc_ensemble in aorc_ensemble_names
    ]

    all_keys_and_paths = mefp_keys_and_paths + westwrf_keys_and_paths + aorc_keys_and_paths

    for key, new_forcings_file_path in tqdm.tqdm(all_keys_and_paths):            
        shutil.copy2(
                os.path.join(new_forcings_file_path, "forcing_por_HHDW1-1.csv"), 
                os.path.join(TARGET_DIR, "forcing_por_HHDW1-1.csv"), 
        )
        shutil.copy2(
                os.path.join(new_forcings_file_path, "forcing_por_HHDW1-2.csv"), 
                os.path.join(TARGET_DIR, "forcing_por_HHDW1-2.csv"), 
        )

        lid = 'HHDW1'

        # 1. Access a the example data
        nwsrfs_sim = simulation.NwsrfsRun.load_example(lid)

        # 2. Print out the configuration
        
        pd.DataFrame(nwsrfs_sim.sim).to_parquet(
            os.path.join(DATA_DIR, f"ensemble_outputs/streamflow_{lid}_{key}.parquet")
        )

    # now that we are done, put back the original forcings
    print("putting back old forcings")
    shutil.copy2(
            os.path.join(ARCHIVE_DIR, "forcing_por_HHDW1-1.csv"),
            os.path.join(TARGET_DIR, "forcing_por_HHDW1-1.csv")
    )
    shutil.copy2(
            os.path.join(ARCHIVE_DIR, "forcing_por_HHDW1-2.csv"),
            os.path.join(TARGET_DIR, "forcing_por_HHDW1-2.csv")
    )

if __name__ == "__main__":
    main()