import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    data = pd.read_csv("all_data.csv")
    return data

def perform_eda(data):
    st.title("Dashboard E-Commerce")

    visualization_option = st.sidebar.selectbox("Pilih Visualisasi", ["Seller City","Customer City", "Review Score Distribution", "Payment Type Distribution", "Orders by Day", "Orders by Hour"])

    if visualization_option == "Seller City":
        # Visualisasi Distribusi Kota Seller
        st.subheader("Kota dengan Seller Terbanyak:")
        top_seller_city = data['seller_city'].value_counts().head(10)
        fig_top_seller = plt.figure(figsize=(10, 6))
        sns.barplot(x=top_seller_city.values, y=top_seller_city.index, palette='viridis')
        plt.title('Top 10 Sebaran Penjual Berdasarkan Kota')
        plt.xlabel('Jumlah Penjual')
        st.pyplot(fig_top_seller)

        st.subheader("Kota dengan Seller Paling Sedikit:")
        tail_seller_city = data['seller_city'].value_counts().tail(10)
        fig_tail_seller = plt.figure(figsize=(10, 6))
        sns.barplot(x=tail_seller_city.values, y=tail_seller_city.index, palette='viridis')
        plt.title('Tail 10 Sebaran Penjual Berdasarkan Kota')
        plt.xlabel('Jumlah Penjual')
        plt.xticks(rotation=45)
        st.pyplot(fig_tail_seller)
    
    elif visualization_option == "Customer City":
        # Visualisasi Distribusi Kota Customer
        st.subheader("Kota dengan Customer Terbanyak:")
        top_customer_city = data['customer_city'].value_counts().head(10)
        fig_top_customer = plt.figure(figsize=(10, 6))
        sns.barplot(x=top_customer_city.values, y=top_customer_city.index, palette='viridis')
        plt.title('Top 10 Sebaran Customer Berdasarkan Kota')
        plt.xlabel('Jumlah Customer')
        st.pyplot(fig_top_customer)

        st.subheader("Kota dengan Customer Paling Sedikit:")
        tail_customer_city = data['customer_city'].value_counts().tail(10)
        fig_tail_customer = plt.figure(figsize=(10, 6))
        sns.barplot(x=tail_customer_city.values, y=tail_customer_city.index, palette='viridis')
        plt.title('Tail 10 Sebaran Penjual Berdasarkan Kota')
        plt.xlabel('Jumlah Customer')
        plt.xticks(rotation=45)
        st.pyplot(fig_tail_customer)

    elif visualization_option == "Review Score Distribution":
        # Visualisasi Review Skor dengan Donut Pie
        st.subheader("Distribusi Review Score:")
        hasil_review = data.groupby(by="review_score").order_id.nunique().sort_index(ascending=False)
        positive = hasil_review.loc[[4, 5]].sum()
        neutral = hasil_review.loc[3]
        bad = hasil_review.loc[[1, 2]].sum()

        st.write("Positive: {}\nNeutral: {}\nBad: {}".format(positive, neutral, bad))

        fig, ax = plt.subplots()
        ax.pie([positive, neutral, bad], labels=['Positive', 'Neutral', 'Bad'], autopct='%1.1f%%',
               startangle=90, colors=['green', 'yellow', 'red'], wedgeprops=dict(width=0.3, edgecolor='w'))
        centre_circle = plt.Circle((0, 0), 0.2, color='white', edgecolor='black', linewidth=1.25)
        ax.add_artist(centre_circle)
        ax.axis('equal') 
        st.pyplot(fig)

    elif visualization_option == "Payment Type Distribution":
        # Visualisasi Distribusi Tipe Payment
        st.subheader("Sebaran Customer Berdasarkan Jenis Payment:")
        payment_dist = data.groupby(by="payment_type").order_id.nunique().sort_values(ascending=False)

        fig, ax = plt.subplots()
        ax.pie(payment_dist, labels=payment_dist.index, autopct='%1.1f%%')
        st.pyplot(fig)

    elif visualization_option == "Orders by Day":
        # Visualisasi Banyaknya Pesanan Berdasarkan Hari
        st.subheader("Banyaknya Pesanan Berdasarkan Hari:")
        orders_by_day = data.groupby(data['order_day'])['order_id'].count().reset_index()
        orders_by_day = orders_by_day.sort_values(by='order_id', ascending=False)
        orders_by_day.rename(columns={'order_day': 'Day', 'order_id': 'order_counts'}, inplace=True)

        fig_orders_by_day = plt.figure(figsize=(10, 4))
        sns.barplot(x='Day', y='order_counts', data=orders_by_day, 
                    order=orders_by_day.sort_values('order_counts', ascending=False)['Day'],
                    palette='viridis')
        plt.title('Banyaknya Pesanan Berdasarkan Hari')
        plt.ylabel('Banyaknya Pesanan')
        plt.xticks(rotation=45)
        st.pyplot(fig_orders_by_day)

    elif visualization_option == "Orders by Hour":
        # Visualisasi Banyaknya Pesanan Berdasarkan Jam (Varchart Horizontal)
        st.subheader("Banyaknya Pesanan Berdasarkan Jam:")
        orders_by_hour = data.groupby('order_hour')['order_id'].count().reset_index()
        orders_by_hour = orders_by_hour.sort_values(by='order_id', ascending=False)
        orders_by_hour.rename(columns={'order_hour': 'Hour', 'order_id': 'order_counts'}, inplace=True)
        orders_by_hour['Hour'] = orders_by_hour['Hour'].apply(lambda x: f'{x:02d}:00')

        fig_orders_by_hour = plt.figure(figsize=(10, 6))
        sns.barplot(x='order_counts', y='Hour', data=orders_by_hour,
                    order=orders_by_hour.sort_values('order_counts', ascending=False)['Hour'])
        plt.title('Banyaknya Pesanan Berdasarkan Jam')
        plt.xlabel('Banyaknya Pesanan')
        plt.yticks(rotation=0)
        st.pyplot(fig_orders_by_hour)

# Sidebar untuk filter atau opsi tambahan
st.sidebar.title("Filter dan Opsi Tambahan")
# Menambahkan filter, opsi, atau parameter tambahan sesuai kebutuhan

# Memuat data
data = load_data()

# Menambahkan EDA dan visualisasi
perform_eda(data)
