# !!!DISCLAIMER!!!
**This Tool is for education/research purposes only. The author takes NO responsibility and/or liability for how you choose to use any of the tools/source code/any files provided.
 The author and anyone affiliated with will not be liable for any losses and/or damages in connection with the use of ANY files provided with This Tool.
 By using AUTOQL or any files included, you understand that you are AGREEING TO USE AT YOUR OWN RISK. Once again ALL files included are for EDUCATION and/or RESEARCH purposes ONLY.
 This tool is ONLY intended to be used on your pen testing labs, or with explicit consent from the owner of the property being tested.**

 # Overview
```
  _______   ___ ___   _______   _______   _______   ___     
 |   _   | |   Y   | |       | |   _   | |   _   | |   |    
 |.  1   | |.  |   | |.|   | | |.  |   | |.  |   | |.  |    
 |.  _   | |.  |   | `-|.  |-' |.  |   | |.  |   | |.  |___ 
 |:  |   | |:  1   |   |:  |   |:  1   | |:  1   | |:  1   |
 |::.|:. | |::.. . |   |::.|   |::.. . | |::..   | |::.. . |
 `--- ---' `-------'   `---'   `-------' `----|:.| `-------'
                                              `--'                                                    
```
 **AUTOQL is a Python-based tool for automated SQL injection testing. It allows you to test SQL injection vulnerabilities in web applications by sending various payloads to specified parameters. 
 The tool supports single and multi-threaded execution and can utilize custom payload files for testing.**

 ## Features ##
- **SQL Injection Testing:** Automatically test for SQL injection vulnerabilities using predefined or custom payloads.
- **Multi-Threading Support:** Speed up testing by using multiple threads.
- **Custom Payload Files:** Load payloads from a custom file for more flexible testing.
- **Detailed Logging:** Log test results, including requests and responses, for later analysis.

# Installation
  - clone the repo to your local machine.
  - Navigate to the project directory.
## **Install the required dependencies**.
    pip install -r requirements.txt 

# Usage

### Basic Usage

You can use the following command to run the script with a target URL and parameters. This will perform single-threaded testing with the specified HTTP method:

```bash
python autoql.py <URL> "<PARAMS>" --method <METHOD>
```
- `<URL>`: The target URL you want to test.
- `<PARAMS>`: Parameters to be tested, formatted as param1=value1,param2=value2. You can specify values for any known parameters. If you know a specific parameter to test, you can set its value; otherwise,
              both parameters will be tested with the payloads. Example: `Username=admin,Password=`
- `<METHOD>`: HTTP method to use (GET or POST).

### Optional Parameters:
`--threads <NUM_THREADS>`: Specify the number of threads to use for multi-threaded testing. Default is 1. Example: `--threads 5`

`--payload-file <FILE_PATH>`: Provide the path to a file containing custom payloads. Example: `--payload-file custom_payloads.txt`


# Examples: #

### Basic ###
```
python autoql.py http://example.com/login "Username=admin,Password=" --method POST
```

### Multi-Threading ###
**For faster testing, you can use multiple threads by specifying the --threads option:**
```
python autoql.py <URL> "<PARAMS>" --method <METHOD> --threads <NUM_THREADS>
```
### Custom Payload File ###

**You can use a custom payload file by providing its path with the --payload-file option:**
```
python autoql.py <URL> "<PARAMS>" --method <METHOD> --payload-file <FILE_PATH>
```

# EXAMPLE #
```
python autoql.py http://example.com/login "Username=admin,Password=" --method POST --payload-file custom_payloads.txt
```

# Coustom file Format #
 ```
' OR '1'='1
' OR '1'='0
' OR 1=1 --
```
