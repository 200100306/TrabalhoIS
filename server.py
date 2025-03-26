import subprocess

def start_rest():
    subprocess.Popen(["python", "rest_api.py"])

def start_soap():
    subprocess.Popen(["python", "soap_api.py"])

def start_graphql():
    subprocess.Popen(["python", "graphql_api.py"])

def start_grpc():
    subprocess.Popen(["python", "grpc_api.py"])

if __name__ == "__main__":
    print("Iniciando os serviços...")
    start_rest()
    start_soap()
    start_graphql()
    start_grpc()
    print("Todos os serviços foram iniciados!")

