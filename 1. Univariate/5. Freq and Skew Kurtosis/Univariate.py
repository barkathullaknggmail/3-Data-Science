class Univariate():
    import pandas as pd

    def qualQuan(dataset):
        quan=[]
        qual=[]
        for cn in dataset.columns:
            if(dataset[cn].dtype == 'O'):
                qual.append(cn)
            else:
                quan.append(cn)
        return qual, quan

    def univeriate(dataset,quan):
        import pandas as pd
        descriptive=pd.DataFrame(index=["Mean","Median","Mode",
                                "Q1:25%","Q2:50%","Q3:75%","Q4:100%",
                                "IQR","1.5Rule","Lesser Outlier","Greater Outlier","Min","Max","skew","kurtosis"],columns= quan)
        for cn in quan:
            descriptive.loc["Mean",[cn]]=dataset[cn].mean()
            descriptive.loc["Median",[cn]]=dataset[cn].median()
            descriptive.loc["Mode",[cn]]=dataset[cn].mode()[0]
            descriptive.loc["Q1:25%",[cn]]=dataset[cn].quantile(0.25)
            descriptive.loc["Q2:50%",[cn]]=dataset[cn].quantile(0.5)
            descriptive.loc["Q3:75%",[cn]]=dataset[cn].quantile(0.75)
            descriptive.loc["Q4:100%",[cn]]=dataset[cn].max()
            
            q1=dataset[cn].quantile(0.25)
            q3=dataset[cn].quantile(0.75)
            iqr=q3-q1
            iqr15=iqr*1.5
            descriptive.loc["IQR",[cn]]=(dataset[cn].quantile(0.75)-dataset[cn].quantile(0.25))
            descriptive.loc["1.5Rule",[cn]]=iqr15
            descriptive.loc["Lesser Outlier",[cn]]=q1-iqr15
            descriptive.loc["Greater Outlier",[cn]]=q3+iqr15 
           
            descriptive.loc["Min",[cn]]=dataset[cn].min()
            descriptive.loc["Max",[cn]]=dataset[cn].max()
            descriptive.loc["skew",[cn]]=dataset[cn].skew()
            descriptive.loc["kurtosis",[cn]]=dataset[cn].kurtosis()            

        return descriptive

    # Find Outlier
    def findoutlier(descriptive,quan):
        lesser=[]
        greater=[]
        for cn in quan:
            if(descriptive[cn]["Min"] < descriptive[cn]["Lesser Outlier"]):
                lesser.append(cn)
            if(descriptive[cn]["Max"]> descriptive[cn]["Greater Outlier"]):
                greater.append(cn)
        return lesser, greater

    # Replace Outliers
    def replceoutlier(dataset,descriptive,lesser,greater,quan):
    # def replceoutlier(dataset,quan):
        import pandas as pd
        # descriptive = Univariate.univeriate(dataset,quan)
        # lesser, greater = Univariate.findoutlier(descriptive,quan)
        for cn in lesser:
            lo=pd.to_numeric(descriptive.loc["Lesser Outlier",[cn]])
            # lo=descriptive.loc["Lesser Outlier",[cn]]
            lo=float(lo.iloc[0])
            dataset.loc[dataset[cn]<=lo,cn]= lo
        for cn in greater:
            go=pd.to_numeric(descriptive.loc["Greater Outlier",[cn]])
            # go=descriptive.loc["Greater Outlier",[cn]]
            go=float(go.iloc[0])
            dataset.loc[dataset[cn]>=go,cn]= go
        return dataset

    
    # Create function of freq_table
    def frequency_table(dataset,cn):
        import pandas as pd
        freq_table= pd.DataFrame(columns=['unquevalue','frequency','relative_frequency','cusum'])
        freq_table['unquevalue']=dataset[cn].value_counts().index
        freq_table['frequency']=dataset[cn].value_counts().values
        freq_table['relative_frequency']=freq_table["frequency"]/(len(freq_table))
        freq_table['cusum']=freq_table["relative_frequency"].cumsum()
        return freq_table