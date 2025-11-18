import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import streamlit as st

class AdvancedSoftReports:
    """Advanced reporting class for detailed software asset analysis"""
    
    def __init__(self, df):
        self.df = df
    
    def create_publisher_analysis(self):
        """Comprehensive publisher analysis"""
        publisher_stats = self.df.groupby('PUBLISHER').agg({
            'NAME': 'nunique',
            'ASSETUUID': 'nunique',
            'PRODUCTNAME': 'nunique',
            'CATEGORY': 'nunique'
        }).reset_index()
        
        publisher_stats.columns = ['Publisher', 'Accounts_Count', 'Assets_Count', 'Products_Count', 'Categories_Count']
        
        # Publisher market share
        total_products = publisher_stats['Products_Count'].sum()
        publisher_stats['Market_Share'] = (publisher_stats['Products_Count'] / total_products * 100).round(2)
        
        return publisher_stats.sort_values('Products_Count', ascending=False)
    
    def create_category_analysis(self):
        """Comprehensive category analysis"""
        category_stats = self.df.groupby('CATEGORY').agg({
            'NAME': 'nunique',
            'ASSETUUID': 'nunique',
            'PRODUCTNAME': 'nunique',
            'PUBLISHER': 'nunique'
        }).reset_index()
        
        category_stats.columns = ['Category', 'Accounts_Count', 'Assets_Count', 'Products_Count', 'Publishers_Count']
        
        # Category diversity
        total_products = category_stats['Products_Count'].sum()
        category_stats['Category_Share'] = (category_stats['Products_Count'] / total_products * 100).round(2)
        
        return category_stats.sort_values('Products_Count', ascending=False)
    
    def create_software_type_analysis(self):
        """Software type distribution analysis"""
        software_type_stats = self.df.groupby('SOFTWARETYPE').agg({
            'NAME': 'nunique',
            'ASSETUUID': 'nunique',
            'PRODUCTNAME': 'nunique',
            'PUBLISHER': 'nunique'
        }).reset_index()
        
        software_type_stats.columns = ['Software_Type', 'Accounts_Count', 'Assets_Count', 'Products_Count', 'Publishers_Count']
        
        return software_type_stats.sort_values('Products_Count', ascending=False)
    
    def create_account_software_matrix(self):
        """Create account-software matrix for heatmap"""
        matrix = self.df.groupby(['NAME', 'PUBLISHER']).size().unstack(fill_value=0)
        return matrix
    
    def create_asset_software_matrix(self):
        """Create asset-software matrix for analysis"""
        matrix = self.df.groupby(['ASSETUUID', 'SOFTWARETYPE']).size().unstack(fill_value=0)
        return matrix
    
    def create_trend_analysis(self):
        """Create trend analysis over accounts"""
        trends = {}
        
        # Publisher trends
        publisher_trends = self.df.groupby(['NAME', 'PUBLISHER']).size().reset_index(name='count')
        trends['publisher'] = publisher_trends
        
        # Category trends
        category_trends = self.df.groupby(['NAME', 'CATEGORY']).size().reset_index(name='count')
        trends['category'] = category_trends
        
        # Software type trends
        software_type_trends = self.df.groupby(['NAME', 'SOFTWARETYPE']).size().reset_index(name='count')
        trends['software_type'] = software_type_trends
        
        return trends
    
    def create_correlation_analysis(self):
        """Create correlation analysis between different metrics"""
        # Create numerical features for correlation
        account_metrics = self.df.groupby('NAME').agg({
            'ASSETUUID': 'nunique',
            'PUBLISHER': 'nunique',
            'CATEGORY': 'nunique',
            'PRODUCTNAME': 'nunique',
            'SOFTWARETYPE': 'nunique'
        }).reset_index()
        
        account_metrics.columns = ['NAME', 'Assets', 'Publishers', 'Categories', 'Products', 'Software_Types']
        
        # Calculate correlation matrix
        correlation_matrix = account_metrics[['Assets', 'Publishers', 'Categories', 'Products', 'Software_Types']].corr()
        
        return correlation_matrix
    
    def create_advanced_visualizations(self):
        """Create advanced visualizations"""
        visualizations = {}
        
        # 1. Publisher market share pie chart
        publisher_stats = self.create_publisher_analysis()
        top_publishers = publisher_stats.head(10)
        
        fig1 = px.pie(top_publishers, values='Products_Count', names='Publisher',
                      title='Top 10 Publishers by Software Count')
        visualizations['publisher_pie'] = fig1
        
        # 2. Category distribution treemap
        category_stats = self.create_category_analysis()
        top_categories = category_stats.head(15)
        
        fig2 = px.treemap(top_categories, path=['Category'], values='Products_Count',
                          title='Software Distribution by Category')
        visualizations['category_treemap'] = fig2
        
        # 3. Account-software heatmap
        matrix = self.create_account_software_matrix()
        top_accounts = matrix.sum(axis=1).nlargest(10).index
        top_publishers = matrix.sum(axis=0).nlargest(10).index
        matrix_subset = matrix.loc[top_accounts, top_publishers]
        
        fig3 = px.imshow(matrix_subset, 
                        title='Account-Software Publisher Heatmap',
                        labels=dict(x="Publisher", y="Account", color="Count"))
        visualizations['account_heatmap'] = fig3
        
        # 4. Software type distribution
        software_type_stats = self.create_software_type_analysis()
        
        fig4 = px.bar(software_type_stats, x='Software_Type', y='Products_Count',
                      title='Software Type Distribution',
                      labels={'Products_Count': 'Number of Products'})
        fig4.update_layout(xaxis_tickangle=-45)
        visualizations['software_type_bar'] = fig4
        
        # 5. Correlation heatmap
        correlation_matrix = self.create_correlation_analysis()
        
        fig5 = px.imshow(correlation_matrix, 
                        title='Correlation Matrix: Account Metrics',
                        labels=dict(x="Metric", y="Metric", color="Correlation"))
        visualizations['correlation_heatmap'] = fig5
        
        return visualizations
    
    def create_drill_down_analysis(self, account=None, publisher=None, category=None):
        """Create drill-down analysis based on filters"""
        filtered_df = self.df.copy()
        
        if account:
            filtered_df = filtered_df[filtered_df['NAME'] == account]
        if publisher:
            filtered_df = filtered_df[filtered_df['PUBLISHER'] == publisher]
        if category:
            filtered_df = filtered_df[filtered_df['CATEGORY'] == category]
        
        # Detailed analysis for filtered data
        analysis = {
            'total_records': len(filtered_df),
            'unique_accounts': filtered_df['NAME'].nunique(),
            'unique_assets': filtered_df['ASSETUUID'].nunique(),
            'unique_publishers': filtered_df['PUBLISHER'].nunique(),
            'unique_categories': filtered_df['CATEGORY'].nunique(),
            'unique_products': filtered_df['PRODUCTNAME'].nunique(),
            'unique_software_types': filtered_df['SOFTWARETYPE'].nunique()
        }
        
        # Top products in filtered data
        top_products = filtered_df['PRODUCTNAME'].value_counts().head(10)
        
        # Publisher distribution in filtered data
        publisher_dist = filtered_df['PUBLISHER'].value_counts().head(10)
        
        # Category distribution in filtered data
        category_dist = filtered_df['CATEGORY'].value_counts().head(10)
        
        return {
            'summary': analysis,
            'top_products': top_products,
            'publisher_distribution': publisher_dist,
            'category_distribution': category_dist
        }
    
    def create_comparative_analysis(self, group1, group2):
        """Create comparative analysis between two groups"""
        # Group 1 analysis
        group1_data = self.df[self.df['NAME'].isin(group1)]
        group1_stats = {
            'accounts': group1_data['NAME'].nunique(),
            'assets': group1_data['ASSETUUID'].nunique(),
            'publishers': group1_data['PUBLISHER'].nunique(),
            'categories': group1_data['CATEGORY'].nunique(),
            'products': group1_data['PRODUCTNAME'].nunique(),
            'software_types': group1_data['SOFTWARETYPE'].nunique()
        }
        
        # Group 2 analysis
        group2_data = self.df[self.df['NAME'].isin(group2)]
        group2_stats = {
            'accounts': group2_data['NAME'].nunique(),
            'assets': group2_data['ASSETUUID'].nunique(),
            'publishers': group2_data['PUBLISHER'].nunique(),
            'categories': group2_data['CATEGORY'].nunique(),
            'products': group2_data['PRODUCTNAME'].nunique(),
            'software_types': group2_data['SOFTWARETYPE'].nunique()
        }
        
        # Create comparison DataFrame
        comparison_df = pd.DataFrame({
            'Group 1': group1_stats,
            'Group 2': group2_stats
        })
        
        # Calculate differences
        comparison_df['Difference'] = comparison_df['Group 2'] - comparison_df['Group 1']
        comparison_df['Percentage_Change'] = ((comparison_df['Group 2'] - comparison_df['Group 1']) / comparison_df['Group 1'] * 100).round(2)
        
        return comparison_df
    
    def export_analysis_results(self, format='csv'):
        """Export analysis results to various formats"""
        results = {
            'publisher_analysis': self.create_publisher_analysis(),
            'category_analysis': self.create_category_analysis(),
            'software_type_analysis': self.create_software_type_analysis(),
            'correlation_matrix': self.create_correlation_analysis()
        }
        
        if format == 'csv':
            for name, data in results.items():
                data.to_csv(f'{name}_analysis.csv', index=False)
        elif format == 'excel':
            with pd.ExcelWriter('software_analysis_results.xlsx') as writer:
                for name, data in results.items():
                    data.to_excel(writer, sheet_name=name, index=False)
        
        return results
