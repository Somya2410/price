import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Laptop Price Comparison",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f4e79;
    }
    .footer {
        margin-top: 3rem;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the laptop dataset"""
    try:
        df = pd.read_csv('attached_assets/Laptop_price_1753901917447.csv')
        
        # Add simulated platform data for demonstration
        platforms = ['Amazon', 'Flipkart', 'Reliance Digital', 'Croma', 'Vijay Sales']
        np.random.seed(42)  # For reproducible results
        df['Platform'] = np.random.choice(platforms, size=len(df))
        
        # Add simulated city data
        cities = ['Bhopal', 'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad']
        df['City'] = np.random.choice(cities, size=len(df))
        
        # Add simulated ratings
        df['Rating'] = np.random.uniform(3.0, 5.0, size=len(df)).round(1)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def create_sidebar_filters(df):
    """Create sidebar filters for the dashboard"""
    st.sidebar.header("Filters")
    
    # City filter
    cities = ['All'] + sorted(df['City'].unique().tolist())
    selected_city = st.sidebar.selectbox("Select City", cities, index=cities.index('Bhopal') if 'Bhopal' in cities else 0)
    
    # Brand filter
    brands = st.sidebar.multiselect(
        "Select Brands",
        options=df['Brand'].unique(),
        default=df['Brand'].unique()[:3]
    )
    
    # Price range filter
    price_range = st.sidebar.slider(
        "Price Range (₹)",
        min_value=int(df['Price'].min()),
        max_value=int(df['Price'].max()),
        value=(int(df['Price'].min()), int(df['Price'].max())),
        step=1000
    )
    
    # Platform filter
    platforms = st.sidebar.multiselect(
        "Select Platforms",
        options=df['Platform'].unique(),
        default=df['Platform'].unique()
    )
    
    # RAM filter
    ram_options = sorted(df['RAM_Size'].unique())
    selected_ram = st.sidebar.multiselect(
        "RAM Size (GB)",
        options=ram_options,
        default=ram_options
    )
    
    # Storage filter
    storage_options = sorted(df['Storage_Capacity'].unique())
    selected_storage = st.sidebar.multiselect(
        "Storage Capacity (GB)",
        options=storage_options,
        default=storage_options
    )
    
    return selected_city, brands, price_range, platforms, selected_ram, selected_storage

def filter_data(df, city, brands, price_range, platforms, ram_sizes, storage_sizes):
    """Apply filters to the dataset"""
    filtered_df = df.copy()
    
    if city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == city]
    
    if brands:
        filtered_df = filtered_df[filtered_df['Brand'].isin(brands)]
    
    filtered_df = filtered_df[
        (filtered_df['Price'] >= price_range[0]) & 
        (filtered_df['Price'] <= price_range[1])
    ]
    
    if platforms:
        filtered_df = filtered_df[filtered_df['Platform'].isin(platforms)]
    
    if ram_sizes:
        filtered_df = filtered_df[filtered_df['RAM_Size'].isin(ram_sizes)]
    
    if storage_sizes:
        filtered_df = filtered_df[filtered_df['Storage_Capacity'].isin(storage_sizes)]
    
    return filtered_df

def create_platform_comparison_chart(df):
    """Create bar chart showing average price per platform"""
    platform_stats = df.groupby('Platform')['Price'].agg(['mean', 'count']).reset_index()
    platform_stats.columns = ['Platform', 'Average_Price', 'Count']
    
    fig = px.bar(
        platform_stats,
        x='Platform',
        y='Average_Price',
        title='Average Laptop Price by Platform',
        color='Average_Price',
        color_continuous_scale='Blues',
        text='Count'
    )
    
    fig.update_traces(texttemplate='%{text} laptops', textposition='outside')
    fig.update_layout(
        xaxis_title="E-commerce Platform",
        yaxis_title="Average Price (₹)",
        showlegend=False,
        height=400
    )
    
    return fig

def create_brand_price_distribution(df):
    """Create box plot showing price distribution per brand"""
    fig = px.box(
        df,
        x='Brand',
        y='Price',
        title='Price Distribution by Brand',
        color='Brand'
    )
    
    fig.update_layout(
        xaxis_title="Brand",
        yaxis_title="Price (₹)",
        showlegend=False,
        height=400
    )
    
    return fig

def create_platform_market_share(df):
    """Create pie chart showing platform market share"""
    platform_counts = df['Platform'].value_counts()
    
    fig = px.pie(
        values=platform_counts.values,
        names=platform_counts.index,
        title='Platform Market Share (by number of laptops)',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    return fig

def create_rating_price_scatter(df):
    """Create scatter plot showing rating vs price"""
    fig = px.scatter(
        df,
        x='Rating',
        y='Price',
        color='Brand',
        size='RAM_Size',
        hover_data=['Platform', 'Storage_Capacity'],
        title='Rating vs Price Analysis',
        opacity=0.7
    )
    
    fig.update_layout(
        xaxis_title="Rating",
        yaxis_title="Price (₹)",
        height=400
    )
    
    return fig

def create_specs_price_analysis(df):
    """Create correlation analysis between specifications and price"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('RAM vs Price', 'Storage vs Price', 'Processor Speed vs Price', 'Screen Size vs Price'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # RAM vs Price
    ram_price = df.groupby('RAM_Size')['Price'].mean().reset_index()
    fig.add_trace(
        go.Scatter(x=ram_price['RAM_Size'], y=ram_price['Price'], mode='lines+markers', name='RAM vs Price'),
        row=1, col=1
    )
    
    # Storage vs Price
    storage_price = df.groupby('Storage_Capacity')['Price'].mean().reset_index()
    fig.add_trace(
        go.Scatter(x=storage_price['Storage_Capacity'], y=storage_price['Price'], mode='lines+markers', name='Storage vs Price'),
        row=1, col=2
    )
    
    # Processor Speed vs Price
    fig.add_trace(
        go.Scatter(x=df['Processor_Speed'], y=df['Price'], mode='markers', name='Processor vs Price', opacity=0.6),
        row=2, col=1
    )
    
    # Screen Size vs Price
    fig.add_trace(
        go.Scatter(x=df['Screen_Size'], y=df['Price'], mode='markers', name='Screen Size vs Price', opacity=0.6),
        row=2, col=2
    )
    
    fig.update_layout(height=600, title_text="Specifications vs Price Analysis", showlegend=False)
    
    return fig

def get_cheapest_platforms(df):
    """Identify the top 2 cheapest platforms"""
    platform_avg_price = df.groupby('Platform')['Price'].mean().sort_values()
    return platform_avg_price.head(2)

def main():
    # Header
    st.markdown('<h1 class="main-header">Laptop Price Comparison in Indian E-commerce</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Explore and compare laptop prices across Amazon, Flipkart, Reliance Digital & more</p>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        st.error("Failed to load data. Please check if the CSV file exists in the correct location.")
        return
    
    # Sidebar filters
    city, brands, price_range, platforms, ram_sizes, storage_sizes = create_sidebar_filters(df)
    
    # Filter data
    filtered_df = filter_data(df, city, brands, price_range, platforms, ram_sizes, storage_sizes)
    
    if filtered_df.empty:
        st.warning("No data available with the selected filters. Please adjust your filters.")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Laptops", len(filtered_df))
    
    with col2:
        st.metric("Average Price", f"₹{filtered_df['Price'].mean():,.0f}")
    
    with col3:
        st.metric("Price Range", f"₹{filtered_df['Price'].min():,.0f} - ₹{filtered_df['Price'].max():,.0f}")
    
    with col4:
        st.metric("Brands Available", filtered_df['Brand'].nunique())
    
    # Cheapest platforms highlight
    st.subheader("Best Deals Alert")
    cheapest_platforms = get_cheapest_platforms(filtered_df)
    
    if len(cheapest_platforms) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🏆 Cheapest: **{cheapest_platforms.index[0]}** - Avg: ₹{cheapest_platforms.iloc[0]:,.0f}")
        with col2:
            st.info(f"🥈 Second Best: **{cheapest_platforms.index[1]}** - Avg: ₹{cheapest_platforms.iloc[1]:,.0f}")
    
    # Visualizations
    st.header("Interactive Analytics Dashboard")
    
    # Row 1: Platform comparison and Brand distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = create_platform_comparison_chart(filtered_df)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = create_brand_price_distribution(filtered_df)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 2: Market share and Rating analysis
    col1, col2 = st.columns(2)
    
    with col1:
        fig3 = create_platform_market_share(filtered_df)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        fig4 = create_rating_price_scatter(filtered_df)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Row 3: Specifications analysis
    fig5 = create_specs_price_analysis(filtered_df)
    st.plotly_chart(fig5, use_container_width=True)
    
    # Data table
    st.header("Detailed Laptop Data")
    
    # Display options
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("Sort by", ['Price', 'Rating', 'RAM_Size', 'Storage_Capacity'])
    with col2:
        sort_order = st.selectbox("Order", ['Ascending', 'Descending'])
    
    # Sort data
    ascending = sort_order == 'Ascending'
    display_df = filtered_df.sort_values(sort_by, ascending=ascending)
    
    # Format display
    display_columns = ['Brand', 'Platform', 'City', 'Price', 'Rating', 'RAM_Size', 'Storage_Capacity', 'Processor_Speed', 'Screen_Size', 'Weight']
    st.dataframe(
        display_df[display_columns].head(20),
        use_container_width=True,
        column_config={
            "Price": st.column_config.NumberColumn("Price (₹)", format="₹%.0f"),
            "Rating": st.column_config.NumberColumn("Rating", format="%.1f ⭐"),
            "RAM_Size": st.column_config.NumberColumn("RAM (GB)", format="%d GB"),
            "Storage_Capacity": st.column_config.NumberColumn("Storage (GB)", format="%d GB"),
            "Processor_Speed": st.column_config.NumberColumn("CPU Speed (GHz)", format="%.2f GHz"),
            "Screen_Size": st.column_config.NumberColumn("Screen (inches)", format="%.1f\""),
            "Weight": st.column_config.NumberColumn("Weight (kg)", format="%.2f kg")
        }
    )
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h3>About This Project</h3>
        <p><strong>Made with ❤️ by Somya Nigam</strong></p>
        <p>
            <a href="https://www.linkedin.com/in/somya-nigam-789408183/" target="_blank">
                LinkedIn Profile
            </a>
        </p>
        <p>Project built using Python & Streamlit</p>
        <hr>
        <p><em>This application provides comprehensive laptop price analysis across major Indian e-commerce platforms. 
        The data is processed to give you insights into pricing trends, brand comparisons, and specification analysis 
        to help you make informed purchasing decisions.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
