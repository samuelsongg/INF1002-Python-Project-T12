import matplotlib.pyplot as plt
import nltk
from assets.dashboard_utils import *

nltk.download('averaged_perceptron_tagger')

def plot_features(data, features):
    num_rows = data.shape[0]
    for column in features:
        st.write(column)
        fig = plt.figure()
        ax = fig.add_subplot()
        subset = data[column]

        if column == "Job Posted Date":
            value_counts = pd.to_datetime(subset, format = "%d/%m/%Y")
            # ax.hist(value_counts)
            # plt.xticks(rotation = 45)
            st.line_chart(value_counts)
            
        else:
            value_counts = subset.value_counts().nlargest(10)
            st.bar_chart(value_counts)


def main():
    st.title("Analysis of Job Descriptions on LinkedIn")
    st.sidebar.header("What Would You Like To Explore?")

    features = st.sidebar.multiselect(
        label = "Select Features To Explore",
        options = ["Company Name", "Job Posted Date", "No. of Employees", "Sector", "Position Level"],
        default = ["Company Name", "Sector"]
    )

    if "data" not in st.session_state:
        with st.spinner("Processing data..."):
            data = clean_data(get_raw_data()).drop(columns = "Job Desc")
            st.session_state["data"] = data
    else:
        data = st.session_state["data"]

    subset = get_filters(data)
    st.dataframe(subset)

    plot_features(subset, features)


main()