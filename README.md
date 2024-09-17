
# FastAPI for revChatVal

A FastAPI server for reverse engineered RMIT Val's API

## Installation
- Download and Install [Python](https://python.org)
- Clone the repository:
```bash
git clone https://github.com/Khang5687/revChatVal.git
git checkout fastapi
cd revChatVal
```
- Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

Set [RMIT Val](https://val.rmit.edu.au) cookies by **one** of two steps:

**Easy**: You can manually insert your own cookies:
  
 - Create `cookies.json` file in the root directory. 
 - Go to [val.rmit.edu.au](https://val.rmit.edu.au) and login.
 - On your browser, look for any cookies that has the key **AppServiceAuthSession**
 - Paste the key name as well as the key value in `cookies.json` as a dictionary 
        
    Its content should look something like this:
    ```python
    {"AppServiceAuthSession": "tqczyJ1ZjZ6..."}
    ```

  **Automated**: If you do not prefer manually entering the cookies, `microsoft_login.py` uses Selenium to automatically extract cookies, provide that you supply it correct login credentials.:
    
*Notes*: `microsoft_login.py` is being reworked, specifically removing Selenium for stability and consistency. 


Run the server on port `8000` (default):
```bash
python run_server.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[GNU General Public License v2.0](https://github.com/Khang5687/revChatVal/blob/fastapi/LICENSE)