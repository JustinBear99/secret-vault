import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def custom_probability(x, mean, std_dev):
    return np.exp(-((x-mean)**2) / (2*std_dev**2)) / (std_dev * np.sqrt(2*np.pi))

st.title('秘密金庫模擬器 (MS Secret Vault Simulator)')

players = st.number_input('參與人數 (Number of players)', min_value=0, value=10000)

chances = st.number_input('機會次數 (Chances per player)', min_value=1, max_value=10, value=5)

max_value = st.number_input('最大值', value=99999)

mean = st.slider('平均 (Mean)', min_value=1, max_value=max_value, value=int(max_value/2), step=10,
                 help='Set the mean of the normal distribution')
std_dev = st.slider('標準差 (Standard Deviation)', min_value=1, max_value=30000, value=5000, step=10,
                    help='Set the standard deviation of the normal distribution')

@st.cache_data
def calculate_distribution(mean, std_dev):
    numbers = np.arange(1, 100000)
    probabilities = custom_probability(numbers, mean, std_dev)
    probabilities /= np.sum(probabilities)
    return numbers, probabilities

numbers, probabilities = calculate_distribution(mean, std_dev)

fig, ax = plt.subplots()
ax.plot(numbers, probabilities)
ax.set_xlabel('數值 (Numbers)')
ax.set_ylabel('機率 (Probability)')
st.pyplot(fig)

def simulate(players, chances, numbers, probabilities):
    st.write('計算中... Calculating...')
    count = [0] * len(numbers)
    for i in range(players * chances):
        r = np.random.choice(numbers, p=probabilities)
        count[r - 1] += 1

    smallest = 0
    for i in range(len(count)):
        if count[i] == 1:
            smallest = i + 1
            break
    st.write(f'贏家是 (Winner is): {smallest}')

if st.button('開始模擬 (Start)'):
    simulate(players, chances, numbers, probabilities)