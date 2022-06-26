def graph_plot(df,year):
    new_df = df[df['year'] == year]
    new_df.dropna(inplace=True)
    new_df['cutoff'] = df['cutoff'].astype(int)
    graph_df = new_df.groupby(['caste', 'list']).max()['cutoff'].reset_index()
    return graph_df