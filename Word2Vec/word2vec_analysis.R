library(tidyr)
library(dplyr)
library(ggplot2)

################
# Similarities #
################
# Alter data frame
w2v_sim_df <- read.csv("w2v_similarities.tsv", sep="\t")
w2v_sim_df <- w2v_df %>% mutate(woman_to_man_leader = woman_leader/man_leader,
                            woman_to_man_strong = woman_strong/man_strong)

# Graphs
ggplot(w2v_df)