# Preprocessor

Preprocessor is a python library for preprocessing the csv file and flattening the json file

  - Preprocess csv file for missing value handling, missing value replacement 
  - Preprocess csv file having textual column for text preprocessing and word normalization
  - Automatically detects the columns data type for csv file and do the preprocessing
  - Flatten any level complex json file .



## Tech

Preprocessor Class :
Preprocessor.preprocessor(file,filetype=None)
###### Parameters:
    - file : str,csv,dict
            File to be preprocessed
    - filetype : str
                Type of the input file.Valid options are either dataframe or json
##### Methods :
Preprocessor.preprocessor.csv_preprocessor(threshold_4_delete_null=0.5,no_null_columns=None,numeric_null_replace=None,textual_column_word_tokenize=False,textual_column_word_normalize=False)
###### Parameters:
    - threshold_4_delete_null : float
                                Ratio of the null values to number of rows
                                
    - no_null_columns :list
                        List of columns which must not have any null values
                        
    - numeric_null_replace : str 
                            Logic for replacement of null values in numeric column. Valid options are mean,median and mode
    
    - textual_column_word_tokenize : Boolean
                                    Whether tokenization of word needed in case of textual column
                                    
    - textual_column_word_normalize : str
                                        Type of normalization of words needed in Textual columns
                                        



