import serpapi
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit.deprecation_util import make_deprecated_name_warning


def compare(med_name):
    params = {
        "engine": "google_shopping",
        "q": med_name,
        "api_key": "076e7fdc0036f28bff0a2137befba50d941fac9fb9423259f51fc467c46afcc4",
        "gl":"in"
    }
    search = serpapi.GoogleSearch(params)
    results=search.get_dict()
    shopping_results=results["shopping_results"]
    return shopping_results

c1,c2=st.columns(2)
c1.image("img.png",width=200)
c2.header("E-pharmacy price comparision system")

"""----------------------------------"""

st.sidebar.title("Enter Name of Medicine:")
med_name=st.sidebar.text_input("Enter Name here:")
number=st.sidebar.text_input("Enter number of options here:")

medicine_company=[]
med_price=[]

if med_name is not None:
    if st.sidebar.button("price compare"):

        shopping_results=compare(med_name)
        lowest_price =float ((shopping_results[0].get("price"))[1:])
        print(lowest_price)
        lowest_price_index = 0
        st.sidebar.image(shopping_results[0].get("thumbnail"))


        for i in range (int(number)):
            current_price=float ((shopping_results[i].get("price"))[1:])
            medicine_company.append(shopping_results[i].get('source'))
            med_price.append(float ((shopping_results[i].get("price"))[1:]))

            """-----------------------------------------------------------------"""


            st.title(f"option{i+1}]")

            c1,c2=st.columns(2)
            c1.write("company:")
            c2.write(shopping_results[i].get('source'))

            c1.write("Title:")
            c2.write(shopping_results[i].get('title'))

            c1.write("Price:")
            c2.write(shopping_results[i].get('price'))

            url=shopping_results[i].get('product_link')

            c1.write("Buy Link:")
            c2.write("[Link](%s)"%url)
            """--------------------------------------------------------------------------------"""
            if (current_price < lowest_price):
                lowest_price = current_price
                lowest_price_index = 1

        # this is best option
        st.title("Best Option")

        c1, c2 = st.columns(2)
        c1.write("company:")
        c2.write(shopping_results[ lowest_price_index].get('source'))

        c1.write("Title:")
        c2.write(shopping_results[ lowest_price_index].get('title'))

        c1.write("Price:")
        c2.write(shopping_results[ lowest_price_index].get('price'))

        url = shopping_results[ lowest_price_index].get('product_link')

        c1.write("Buy Link:")
        c2.write("[Link](%s)" % url)

        #--------------------
        # graph comparision
        df=pd.DataFrame(med_price,medicine_company)
        st.title("Chart Comparision:")
        st.bar_chart(df)


        fig,ax=plt.subplots()
        ax.pie(med_price,labels=medicine_company,shadow=True)
        ax.axis("equal")
        st.pyplot(fig)

