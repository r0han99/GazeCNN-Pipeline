import pandas as pd 
import argparse



def fetch_records(file):

    data = pd.read_csv(file)

    return data.shape[0]





if __name__ == '__main__':
    
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--file")
    args = parser.parse_args()


    count = fetch_records(args.file)

    print(f'Number of Samples: {count}')
    


    