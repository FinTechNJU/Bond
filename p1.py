# %%
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
    def attribute(self, name):
        if name not in self._attributes:
            self._attributes[name] = Attribute()
        return self._attributes[name]    
    def set_r(self, r):
        self.r = r
        return self.r

class Bondbook:
    def __init__(self):
        self._bonds = {}
    def bond(self, name):
        if name not in self._bonds:
            self._bonds[name] = Bond()
        return self._bonds[name]
# �����Ǻ���
class Get_Attributes:
    @staticmethod
    def get_r( interest_list, price, T):
        # r = (sum(interest_list) - price) / (price * T)
        r = 0.02277500
        return r 
    @staticmethod
    def get_C1(stock, r):
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
        T = len(stock) / 250 
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

class Global_Functions:
    @staticmethod
    def set_up(i, K):
        # ��ʼ��ÿһ��ծȯ
        bond_price = dfRaw.iloc[:,i]
        bond_name = pd.DataFrame(dfRaw.iloc[:,i]).columns.tolist()[0]
        stock = dfRaw2.iloc[:,i]
        # ���п�תծ
        bond1 = book.bond(bond_name)
        # ʾ����һ����תծ����
        book.bond(bond_name).set_r(Get_Attributes.get_r(list1, bond_price , len(stock)))
        # ����r��ֵ
        bond1.attribute('T').add_value(len(stock))
        bond1.attribute('K').add_value(K)
        bond1.attribute('C1').add_value(Get_Attributes.get_C1(stock, book.bond(bond_name).r))
        bond1.attribute('C2').add_value((Get_Attributes.get_C2(list1, book.bond(bond_name).r)))
        # ���ò�ͬ���Ե�ֵ
        value = book.bond(bond_name).attribute('C1').value() + book.bond(bond_name).attribute('C2').value()
        bond1.attribute('Arbitrage').add_value(value - bond_price)
        # ���ÿ�תծ����������
    @staticmethod
    def show_info(i):
        bond_name = pd.DataFrame(dfRaw.iloc[:,i]).columns.tolist()[0]
        temp = book.bond(bond_name).attribute('Arbitrage').value()
        print(temp)
        # �����תծ�������ռ�
        temp.to_csv('./output/'+bondname+'.csv',mode='w+')
        # ��תծ�������ռ䱣��Ϊcsv�ļ�


if __name__=='__main__':
    # ������ 
    if (len(dfRaw)==0) or (len(dfRaw2)==0):
        dfRaw, dfRaw2 = read_data()
    # �������

    r = 0.02277500 # 2020��5��27�յ������ڵĹ�ծ������
    # ���е��ڿɻ�������ʣ�[ծȯ�ֺ�, ���ڵ����]�����㵽����
    q = 0
    book = Bondbook()
    # ���ÿ�תծ�Ļ���ָ��
    # �������п�תծ

    list1=[0.4, 0.6, 1.0, 1.6, 2.0, 112.5] # ծȯ1����Ϣ��
    K1 = 37.97 # ծȯ1����Ȩ��
    list2=[0.4, 0.6, 1.0, 1.6, 2.0, 112.5]
    # ����ÿһ����תծ

    Global_Functions.set_up(0, K1)
    Global_Functions.show_info(0)













# %%
# class Test:
#     @staticmethod
#     def f(x):
#         return x+3
# a = Test.f(2)