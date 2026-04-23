import requests
import pandas as pd
import os
import json
import fsystem 

from file_manager import DATA_DIR as fdr
with requests.Session() as session:
    response = requests.get('https://fakestoreapi.com/products?limit=5')
    fsystem.init_fsys()

    if response.status_code == 200:
        
        product = response.json()
        fp=os.path.join(fdr,"fakestore")

        print(fp)

        with open(fp,'w', encoding='utf-8') as f :
        
            json.dump(product, f, indent=4)
        
        df=pd.DataFrame(product)
        # for item in product:
        #     print(f" product: {item['title']} | Price: ${item['price']}")

        # print(df.head)
    else:
        
        print("failed to connect to the store")


