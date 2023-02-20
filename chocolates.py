import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px


# Streamlit Stuff
# Define page title, icon, layout and sidebar state
st.set_page_config(page_title="Chocolates of the World", page_icon=":chocolate_bar:",
                   layout="wide", initial_sidebar_state="expanded")

# Create sidebar
st.sidebar.title("Chocolates of the World")
st.sidebar.write(
    "Fonte: https://www.kaggle.com/datasets/rtatman/chocolate-bar-ratings")

# Define header and subheader
st.markdown("<h1 style='text-align: center; '>Choco World</h1>",
            unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; '>Chocolate Scraping with Beautiful Soup</h3>",
            unsafe_allow_html=True)


# get the html
html_page = requests.get(
    "https://content.codecademy.com/courses/beautifulsoup/cacao/index.html")

# Create a BeautifulSoup object
soup = BeautifulSoup(html_page.content, "html.parser")


st.write("How many terrible chocolate bars are out there? And how many earned a perfect 5? Let's make a histogram of this data.")

# Get the ratings
soup_ratings = soup.find_all(attrs={"class": "Rating"})

ratings = []

for rating in soup_ratings[1:]:
    ratings.append(float(rating.get_text()))

# Plot the ratings adding the title and axis labels
plt.hist(ratings)
plt.title("Ratings of Chocolate Bars")
plt.xlabel("Rating")
plt.ylabel("Number of Bars")
plt.show()


# Get the company names
soup_company = soup.find_all(attrs={"class": "Company"})
company_names = []
for name in soup_company[1:]:
    company_names.append(name.get_text())

# Create a DataFrame with the company names and ratings
df = pd.DataFrame({"Company": company_names, "Ratings": ratings})

# Group the DataFrame by company and take the mean of the ratings
mean_vals = df.groupby("Company").Ratings.mean().nlargest(10)
print(mean_vals)

# Get the cocoa percentage
soup_cocoa = soup.find_all(attrs={"class": "CocoaPercent"})

# Create a list with cocoa percentages
cocoa_percentages = []

# Loop through the soup_cocoa list and get the text
for percent in soup_cocoa[1:]:
    # Remove the % sign from the text
    percent = percent.get_text().replace("%", "")
    # Convert the text into a float
    cocoa_percentages.append(float(percent))

# Add the cocoa percentages to the DataFrame
df["CocoaPercentage"] = cocoa_percentages

# Clear the figure
plt.clf()

# Plot the DataFrame with the x-axis as the cocoa percentages and the y-axis as the ratings
plt.scatter(df.CocoaPercentage, df.Ratings)
plt.title("Ratings vs Cocoa Percentage")
plt.xlabel("Cocoa Percentage")
plt.ylabel("Rating")
plt.show()

# Check if there is a relationship between the cocoa percentage and the ratings with labels and title
z = np.polyfit(df.CocoaPercentage, df.Ratings, 1)
line_function = np.poly1d(z)
plt.plot(df.CocoaPercentage, line_function(df.CocoaPercentage), "r--")
# Add the x-axis and y-axis labels
plt.xlabel("Cocoa Percentage")
plt.ylabel("Rating")

plt.show()

# Get the locations of the chocolate bars with the highest ratings
soup_location = soup.find_all(attrs={"class": "CompanyLocation"})
locations = []

for location in soup_location[1:]:
    locations.append(location.get_text())

# Add the locations to the DataFrame
df["Company Location"] = locations

# Add bars names to the DataFrame
soup_bar = soup.find_all(attrs={"class": "Origin"})
bar_names = []

for bar in soup_bar[1:]:
    bar_names.append(bar.get_text())

df["Bar Name"] = bar_names

# Which countries produce the highest-rated bars?
top_ten = df.groupby("Company Location").Ratings.mean().nlargest(10)

# Plot the top ten countries with the highest-rated bars
sns.barplot(x=top_ten.index, y=top_ten)
plt.title("Top Ten Countries with Highest-Rated Bars")
plt.ylabel("Average Rating")
plt.xlabel("Company Location")
plt.show()

# Top 10 bars per rating, company, and location
top_ten_bars = df.nlargest(10, "Ratings")
top_ten_bars

# Top Brazilian bars
brazil_bars = df[df["Company Location"] == "Brazil"].nlargest(10, "Ratings")
brazil_bars

# Where the companies are located in percentage (pie chart)
locations = df["Company Location"].value_counts()
locations

# Plot the locations using pie chart seaborn
plt.clf()
sns.set_style("darkgrid")
plt.figure()
plt.title("Locations of Chocolate Bars")
plt.pie(locations, labels=locations.index, autopct="%1.0f%%")
plt.axis("equal")
plt.show()


# FOOTER
# Footer
def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """

    style_div = styles(
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        # width=percent(100),
        text_align="center",
        # height="60px",
        # opacity=0.6
    )

    style_hr = styles(
    )

    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "<b>Made with ❤️ by</b> ",
        link("https://www.arkhad.com/", " xJuggl3r"),

        " using Python ",
        link("https://www.python.org/", image('https://i.imgur.com/ml09ccU.png',
                                              width=px(18), height=px(18), margin="0em")),
        ", Streamlit ",
        link("https://streamlit.io/", image('https://streamlit.io/images/brand/streamlit-mark-color.svg',
                                            width=px(24), height=px(25), margin="0em")),
    ]
    layout(*myargs)


if __name__ == "__main__":
    footer()
