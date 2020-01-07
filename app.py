import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder
@st.cache
def get_data(csv_file):
	df = pd.read_csv(csv_file)
	return df

def main():
	html_temp = """
	<div style="background-color:white;"><p style="color:black;text-align:center;font-size:50px;padding:20px">UNDERSTAND YOUR DATA</p></div>
	"""
	html_line = """<hr />"""
	st.markdown(html_temp,unsafe_allow_html=True)

	csv_file = st.file_uploader("Upload Your CSV", type=["csv"])
	if csv_file is not None:
		df = get_data(csv_file)
		if st.checkbox("Show Dataset"):
			head_tail = st.radio("Show Data From", ("Head", "Tail"))
			if head_tail == 'Head':
				st.text("Head")
				number = st.number_input("Number of rows", 1, round(df.shape[0] / 2))
				st.dataframe(df.head(number))
			elif head_tail == 'Tail':
				number = st.number_input("Number of rows", 1, round(df.shape[0] / 2))
				st.dataframe(df.tail(number))
			else:
				number = st.number_input("Number of rows", 1, df.shape[0])
				st.dataframe(df.head(number))
			st.markdown(html_line, unsafe_allow_html=True)

		if st.checkbox("Show Column Names and Data Types"):
			st.text('Columns and Data Types')
			st.write(df.dtypes)
			st.markdown(html_line, unsafe_allow_html=True)

		if st.checkbox("Select Columns to Show"):
			all_columns = df.columns.tolist()
			selected_columns = st.multiselect("Select",all_columns)
			st.dataframe(df[selected_columns])
			st.markdown(html_line, unsafe_allow_html=True)

		if st.checkbox("Show Value Counts of Column"):
			all_columns = df.columns.tolist()
			selected_columns = st.selectbox("Select a Column", all_columns)
			if selected_columns is not None:
				st.write(df[selected_columns].value_counts())
			st.markdown(html_line, unsafe_allow_html=True)

		if st.checkbox("Show Summary"):
			st.write(df.describe().T)
			st.markdown(html_line, unsafe_allow_html=True)

		graphlayout = go.Layout(
			margin={'l': 15, 'r': 40, 'b': 20, 't': 10},
			plot_bgcolor='rgba(255,255,255,0.0)',
			paper_bgcolor='rgba(255,255,255,0.0)',
			font={'color': '#000000', 'size': 10},
		)

		st.header("Visualization")
		if st.checkbox("Correlation Plot (Heatmap)"):
			encoder = LabelEncoder()
			newdf = df.copy()
			object_df = newdf.select_dtypes(include=['object'])
			for col in object_df.columns:
				newdf[col] = encoder.fit_transform(object_df[col])
			del object_df
			fig = go.Figure(data=go.Heatmap(
				z=newdf.corr().values.tolist(),
				x=newdf.columns,
				y=newdf.columns,
				hoverongaps=False,colorscale='Viridis'))
			st.plotly_chart(fig)
			st.markdown(html_line, unsafe_allow_html=True)

		st.subheader("Customizable Plot")

		type_of_plot = st.selectbox("Select Type of Plot",["Histogram","Bar","Scatter","Box"])
		all_columns_names = df.columns.tolist()
		if type_of_plot =='Histogram':
			selected_x_column = st.selectbox("Select X Column",all_columns_names)
		if type_of_plot == 'Box':
			selected_y_column = st.selectbox("Select Y Column", all_columns_names)
		if type_of_plot =='Bar':
			selected_x_column = st.selectbox("Select X Column", all_columns_names)
			selected_y_column = st.selectbox("Select Y Column", all_columns_names)
		if type_of_plot == 'Scatter':
			selected_x_column = st.selectbox("Select X Column", all_columns_names)
			selected_y_column = st.selectbox("Select Y Column", all_columns_names)
			selected_type = st.selectbox("Select Type", ['markers', 'lines', 'lines+markers'])

		if type_of_plot == 'Bar':
			fig = go.Figure(data=[go.Bar(x=df[selected_x_column], y=df[selected_y_column])],
							layout=graphlayout)
			st.plotly_chart(fig)

		if type_of_plot == 'Scatter':
			if selected_type is not None:
				fig = go.Figure(data=[go.Scatter(x=df[selected_x_column], y=df[selected_y_column], mode=selected_type)],
								layout=graphlayout)
				st.plotly_chart(fig)

		if type_of_plot == 'Histogram':
			fig = go.Figure(data=[go.Histogram(x=df[selected_x_column])],
							layout=graphlayout)
			st.plotly_chart(fig)

		if type_of_plot == 'Box':
			fig = go.Figure(data=[go.Box(y=df[selected_y_column])],
							layout=graphlayout)
			st.plotly_chart(fig)

		st.sidebar.header("About App")
		st.sidebar.info("This application was made for the analysis of small data.")

		st.sidebar.header("Application Codes")
		st.sidebar.info("http://github.com/buraketmen/StDemo")

		st.sidebar.header("About")
		st.sidebar.info("buraketmen@gmail.com")


if __name__ == '__main__':
	main()
