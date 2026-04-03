import sys
import logging
#from logger_config import setup_logging
# from file_manager import ensure_directories
import gc
import fsystem
# 1. Import your sub-modules
import etl_sales
import etl_inventory
import sales2

fsystem.init_fsys()

logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for the PandasP ETL Project.
    Supports command line arguments: 'sales', 'inventory', or 'all'.
    """
    logger.info("==========================================")
    logger.info("--- PandasP ETL Orchestrator Started ---")
    logger.info("==========================================")

    # Determine which task to run from command line (e.g., python main.py sales)
    task = sys.argv[1] if len(sys.argv) > 1 else "all"
    logger.info(f"Target Task identified: {task.upper()}")

    try:
        if task == "sales":
            logger.info("Starting Sales Pipeline...")
            etl_sales.run_sales_pipeline()
            
        elif task == "inventory":
            logger.info("Starting Inventory Pipeline...")
            etl_inventory.run_inventory_pipeline()

        elif task == "sales2":
            logger.info("Starting sales 2")
            sales2.run_sales_pipleine()
            
        else:
            # Default: Run the full suite
            logger.info("Starting Full ETL Suite (Sales + Inventory)...")
            etl_sales.run_sales_pipeline()
            etl_inventory.run_inventory_pipeline()

        logger.info("--- Orchestrator: All tasks completed successfully ---")
        collected = gc.collect()

    except Exception as e:
        # This catches any crash in the pipelines and logs it to your daily file
        logger.critical(f"FATAL ERROR during ETL Orchestration: {str(e)}", exc_info=True)
        sys.exit(1) # Exit with error code for Docker/Azure visibility

# The "Switch" that triggers the main function
if __name__ == "__main__":
    main()