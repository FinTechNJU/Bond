# %%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats
import collections
dfRaw, dfRaw2 = pd.DataFrame(), pd.DataFrame()
# ȫ�ֱ���
# ����������
class Attribute:
    def __init__(self):
        self._values = []
    
    def add_value(self, value):
        self._values.append(value)
    
    def value(self):
        return self._values[0]

class Bond:
    def __init__(self):
        self._attributes = {}
        self.r = np.nan
        self.T = np.nan
    def attribute(self, name):
        if name not in self._attributes:
            self._attributes[name] = Attribute()
        return self._attributes[name]    
    def set_r(self, r):
        self.r = r
        return self.r
    def set_T(self, T):
        self.T = T
        return self.T

class Bondbook:
    def __init__(self):
        self._bonds = {}
    def bond(self, name):
        if name not in self._bonds:
            self._bonds[name] = Bond()
        return self._bonds[name]
# ============================================================================== #
# �����Ǻ���
class GetAttributes:
    @staticmethod
    def get_r( interest_list, price, T):
        # r = (sum(interest_list) - price) / (price * T)
        # r = 0.02277500
        r = np.power(sum(interest_list)/100, 1/6) - 1
        return r 
    @staticmethod
    def get_T( stock):
        # ����Ҫ���Ʊ�Ŀ�ʼʱ������ծȯ�Ŀ�ʼʱ����ͬ
        total_year_length = 6
        passed_year_length = len(stock)/250
        T = total_year_length - passed_year_length
        return T
    @staticmethod
    def get_C1(stock, r, K, T):
        def get_sigma(stock): 
            stock_ln = np.log(stock)
            miu = stock_ln.diff()
            miu = miu.iloc[1:]
            miu_avr = miu.mean()
            total=0
            for i in range(len(miu)):
                total += np.power(miu.iloc[i] - miu_avr,2)
            sigma = np.sqrt(total/(len(miu)-1))
            sigma_total = sigma * np.sqrt(250)
            return sigma, sigma_total
        def especially_small(C):
            for i, item in enumerate(C.values.tolist()):
                if item < 1e-4:
                    C.iat[i] = 0
            return C
        sigma, sigma_y = get_sigma(stock)
        up = np.log(stock / K) + T * (r - q + np.power(sigma,2)/2)
        down = sigma * np.sqrt(T)
        d1 = up / down
        d2 = d1 - down
        C = stock * stats.norm(0,1).cdf(d1) - K* np.exp(-1*r*T) * stats.norm(0,1).cdf(d2)
        C = especially_small(C)
        return C
    @staticmethod
    def get_C2(interest_list, r):
        def f(l,n):
            return l/np.power(1 + r,n)
        total = 0 
        for i, item in enumerate(interest_list):
            l = item
            n = i+1
            total += f(l,n)
        return total
    @staticmethod
    def get_Value_Series(K, stock):
        Value_Series = (100/K) * stock
        return Value_Series
    @staticmethod
    def get_Premium_Rate(bond_price, Value_Series):
        Premium_Rate = (bond_price - Value_Series)/ Value_Series
        return Premium_Rate
class GlobalFunctions:
    @staticmethod
    def set_up(i, K):
        # ��ʼ��ÿһ��ծȯ
        bond_price = dfRaw.iloc[:,i]
        bond_name = pd.DataFrame(dfRaw.iloc[:,i]).columns.tolist()[0]
        stock = dfRaw2.iloc[:,i]
        # ���п�תծ
        bond1 = book.bond(bond_name)
        # ʾ����һ����תծ����
        book.bond(bond_name).set_r(GetAttributes.get_r(list1, bond_price , len(stock)))
        book.bond(bond_name).set_T(stock)
        # ����r��T��ֵ
        bond1.attribute('T').add_value(GetAttributes.get_T(stock))
        bond1.attribute('K').add_value(K)
        bond1.attribute('C1').add_value(GetAttributes.get_C1(stock, book.bond(bond_name).r, K, book.bond(bond_name).T))
        bond1.attribute('C2').add_value((GetAttributes.get_C2(list1, book.bond(bond_name).r)))
        # ���ò�ͬ���Ե�ֵ
        value = book.bond(bond_name).attribute('C1').value() + book.bond(bond_name).attribute('C2').value()
        bond1.attribute('Arbitrage').add_value(value - bond_price)
        # ���ÿ�תծ����������
        book.bond(bond_name).attribute('Value_Series').add_value(GetAttributes.get_Value_Series(K, stock))
        # ���ÿ�תծ��ת�ɼ�ֵ
        book.bond(bond_name).attribute('Premium_Rate').add_value(GetAttributes.get_Premium_Rate(bond_price, book.bond(bond_name).attribute('Value_Series').value()))
        # ���ÿ�תծ��ת�������
        book.bond(bond_name).attribute('Stock_Price').add_value(stock)
        # �������ɹɼ�
    @staticmethod
    def save_info(i):
        bond_name = pd.DataFrame(dfRaw.iloc[:,i]).columns.tolist()[0]
        temp = book.bond(bond_name).attribute('Arbitrage').value()
        # print(temp)
        # �����תծ�������ռ�
        temp.to_csv('./output/'+bond_name+'.csv',mode='w+')
        # ��תծ�������ռ䱣��Ϊcsv�ļ�
        print("Done")
    @staticmethod
    def read_data():
        dfRaw = pd.read_csv('./excel1.csv',encoding='gbk').set_index('DateTime')
        dfRaw2 = pd.read_csv('./excel2.csv',encoding='gbk').set_index('DateTime')
        return dfRaw, dfRaw2
    @staticmethod
    def draw_scatter(i):
        # ���ɹɼۺ�����ʵ�ɢ��ͼ
        bond_name = pd.DataFrame(dfRaw.iloc[:,i]).columns.tolist()[0]
        temp_bond = book.bond(bond_name) # ���ָ��ծȯ��ʵ��
        x = temp_bond.attribute('Stock_Price').value()
        y = temp_bond.attribute('Premium_Rate').value()
        plt.scatter(x, y)
        plt.xlabel('Stock_Price')
        plt.ylabel('Premium_Rate')
        plt.show()
    @staticmethod
    def draw_line(i):
        bond_name = pd.DataFrame(dfRaw.iloc[:,i]).columns.tolist()[0]
        temp_bond = book.bond(bond_name) # ���ָ��ծȯ��ʵ��
        y1_series = temp_bond.attribute('Stock_Price').value() # ���ɼ۸�
        y2_series = temp_bond.attribute('Value_Series').value() # ת�ɼ�ֵ
        time_line = y1_series.index.tolist() # ʱ������
        y1 = y1_series.values.tolist()
        y2 = y2_series.values.tolist()
        plt.plot(time_line, y1, label = 'Stock_Price')
        plt.plot(time_line, y2, label = 'Value_Series')
        plt.legend()
        plt.show()
# ============================================================================== #

if __name__=='__main__':
    # ������ 
    if (len(dfRaw)==0) or (len(dfRaw2)==0):
        dfRaw, dfRaw2 = GlobalFunctions.read_data()
    # �������

    q = 0 # qӦ�����ó�ʲô����Ҳ��֪��
    book = Bondbook()
    # ���ÿ�תծ�Ļ���ָ��
    # �������п�תծ

    list1=[0.4, 0.6, 1.0, 1.6, 2.0, 112.5] # ծȯ1����Ϣ��
    K1 = 37.97 # ծȯ1����Ȩ��
    list2=[0.4, 0.6, 1.0, 1.6, 2.0, 112.5]
    K2 = 20.22 # ծȯ2����Ȩ��
    # ����ÿһ����תծ

    GlobalFunctions.set_up(0, K1)
    GlobalFunctions.save_info(0)
    GlobalFunctions.draw_scatter(0)
    GlobalFunctions.draw_line(0)

# %%
