import pandas as pd

df = pd.read_csv('C:\develop\Fishing_team\data\dataset.csv')

df['device_type'] = df['device_type'].replace({
    'atm': 'ATM', 
    'ATM': 'ATM', 
    'pos trm': 'port_trm', 
    'prtbl trm': 'port_trm', 
    'port_trm': 'port_trm', 
    'Portable term': 'port_trm'
})

df['oper_type'] = df['oper_type'].replace({
    'in': 'add_on_acc', 
    'in_acc': 'add_on_acc', 
    'out': 'add_on_acc', 
    'add_on_acc': 'add_on_acc', 
    'from_acc': 'decrease_on_acc', 
    'decrease_on_acc': 'decrease_on_acc', 
    'diff_cntry': 'country_transfer', 
    'country_transfer': 'country_transfer', 
    'err': 'err_code', 
    'err_code': 'err_code', 
    'bad': 'err_code'
})

df.to_csv('processed_data.csv', index=False)
