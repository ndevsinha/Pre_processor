# Preprocessor

Preprocessor is a python library for preprocessing the csv file and flattening the json file

  - Preprocess csv file for missing value handling, missing value replacement 
  - Preprocess csv file having textual column for text preprocessing and word normalization
  - Automatically detects the columns data type for csv file and do the preprocessing
  - Flatten any level complex json file .



## Documentation

##### Preprocessor Class :
>Preprocessor.preprocessor(file,filetype=None,encoding=None)
###### Parameters:
    - file : str,csv,dict
            File to be preprocessed
    - filetype : str
                Type of the input file.Valid options are either dataframe or json
    - encoding : str
                encoding scheme for reading file.Default is ISO-8859-1
##### Methods :
>Preprocessor.preprocessor.csv_preprocessor(threshold_4_delete_null=0.5,no_null_columns=None,
numeric_null_replace=None,textual_column_word_tokenize=False,textual_column_word_normalize=False)
###### Parameters:
    - threshold_4_delete_null : float
                        Ratio of the null values to number of rows for columns to be deleted.
    - no_null_columns :list
                        List of columns which must not have any null values
    - numeric_null_replace : dict 
                        Logic for replacement of null values in numeric column. When None all
                        numeric column's null value will be replaced by mean. Dict format 
                        should be {"mean":[list of column name],"median":[list of 
                        columname],"mode":[list of column names]}
                        In case of giving input as dict format, users need to provide 
                        exaustivelist of column combining all three keys mean,median and mode.
    
    - textual_column_word_tokenize : Boolean
                        Whether tokenization of word needed in case of textual column
    - textual_column_word_normalize : str
                        Type of normalization of words needed in Textual columns.Either stem 
                        or lemma for word stemming and word lemmatization respectively.



>Preprocessor.preprocessor.json_preprocessing()
###### parameters
    -No parameters needed

## Code Samples
##### csv file preprocessing using file path
```python
from Pre_processor import preprocessor
pps = preprocessor(file="example.csv")
data = pps.csv_preprocessor(threshold_4_delete_null=0.7,textual_column_word_tokenize=True)
```
