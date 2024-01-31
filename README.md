# Dimension Estimation

Estimate the intrinsic dimension of a dataset based upon [Dimension estimation using random connection models](https://dl.acm.org/doi/10.5555/3122009.3208019) by Paulo Serra and Michel Mandjes.

The basis of the python backend to website connection is very similar to my [Numerical ODE Visualizer](https://github.com/MichelKrispin/NumericalODEVisualizer) and more generally to [wepps](https://github.com/Parallel-in-Time/wepps).


## Usage

The project can be started by making a virtual environment, installing the python dependencies, runing the main file and then opening a browser at `http://127.0.0.1:8000`.
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./main.py
```

### Custom data

Data can be edited by simply copying one of the files in the `data/` folder (but not the `fetch.py` file) and then editing its content.
The new file name should be descriptive as it is used by the frontend and the function name should not be changed, i.e., it has to be equal to `get_data` with the given arguments.

After refreshing the webpage, any new data file should be seen in the frontend.
