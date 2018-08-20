##Summarize ARFF files from experiment-1 and experiment-2

install.packages("farff")
library(farff)

setwd("C://Users//Chris//Documents//GitHub//DW_Microtasks//output//");
experiment1_fileName = "consolidated_Final_Experiment_1.arff";
experiment2_fileName = "consolidated_Final_Experiment_2.arff"

data_1 <- readARFF(experiment1_fileName, data.reader = "readr", tmp.file = tempfile(), show.info = TRUE)

data_1 <- data_1[complete.cases(data_1), ]

head(data_1)

summary(data_1)
