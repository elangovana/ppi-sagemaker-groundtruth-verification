# SageMaker GroundTruth  - PPI extraction verification
This is a sample template for SageMaker  ground truth solution for verifying PPI extraction. 
This has 3 components
1. The HTML template that the workers will use to work on the task
1. Lambda functions for pre and post processing rules.

**Note** This template currently only supports one type of entity

![Preview](docs/preview.png)



## Setup
1. If you want try this sample but dont have the data to test this, you cam use this a sample file [tests/sample_input_data_pubtator.txt](tests/sample_input_data_pubtator.txt) as input data to evaluate the workflow.

1. Create pre and post processing lambda functions
    - **Note** Using the naming convention SageMaker-* for your lambda functions automatically gives access to Sagemaker using the standard template. Otherwise you would have to use create an IAM policy and provide access to Sagemaker to execute the lambda function
   
    - Create a lambda function SageMaker-PPIPreProcessing with runtime python 3.7 using the code [source/lambda_preprocess/preprocess_handler.py](source/lambda_preprocess/preprocess_handler.py). 
   
    - Create a lambda function SageMaker-PPIPostProcessing with runtime python 3.7 using the code [source/lambda_postprocess/postprocess_handler.py](source/lambda_postprocess/postprocess_handler.py). Make sure this has access to read the s3 bucket containing the results from Sagemaker groundtruth job you are about to create

1. Configure SageMaker Ground Truth as follows:
  
   - Choose custom template in Sagemaker Ground Truth
  
   - In the custom template section, copy paste the html from [source/template/template.html](source/template/template.html)
   
   - In the Pre-labelling task lambda function, select Sagemaker-PPIPreProcessing
   
   - In the Post-labelling task lambda function, select Sagemaker-PPIPostProcessing

![setup](docs/setup_custom_template.png)

 

## Run tests

```bash
export PYTHONPATH=./source
pytests
```
