class Univariate():
    def qualQuan(dataset):
        qual =[]
        quan =[]
        for cn in dataset.columns:
            if(dataset[cn].dtype == 'O'):
                qual.append(cn)
            else:
                quan.append(cn)
        return qual, quan
