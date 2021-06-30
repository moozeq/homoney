# homoney

Flask-based application for manging your home budget.

# Run

```bash
git clone https://github.com/moozeq/homoney.git

# prepare environment
cd homoney
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

# add config
echo '{"ENV": "production", "HOST": "127.0.0.1", "PORT": 5000}' > cfg.json

# run app
./homoney.py -c cfg.json
```

App should be available at [127.0.0.1:5000](http://127.0.0.1:5000)
