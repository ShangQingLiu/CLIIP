from CLIIP_module.ensemble_learning import Ensemble_model
from CLIIP_module.CLIIP_process import CLIIP_process
if __name__ == "__main__":
    # process start create all data and simulation
    CLIIP_process()
    # ensemble learning
    ensemble_model = Ensemble_model()
    ensemble_model.import_data()
    ensemble_model.incubation_update()
    ensemble_model.ensemble_lightGBM()


    print(f"ensemble_model.varX:{ensemble_model.varX}")
