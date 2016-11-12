library(tidyr)
library(dplyr)
library(ggplot2)

################
# Similarities #
################
w2v_sim_df <- read.csv("similarities.tsv", sep="\t")
w2v_sim_df <- filter(w2v_sim_df, topic != "Technology")
w2v_sim_df <- w2v_sim_df %>% mutate(woman_to_man_leader = woman_leader/man_leader,
                                    woman_mother_to_man_father = woman_mother/man_father,
                                    woman_to_man_strong = woman_strong/man_strong,
                                    woman_to_man_weak = woman_weak/man_weak)

# Graphs
## Leader: Woman
ggplot(w2v_sim_df, aes(x = year, y = woman_leader, group = topic, color = topic)) +
  geom_line() +
  theme(legend.position = "bottom", legend.title = NULL) +
  ylim(0,1)

## Leader: Man
ggplot(w2v_sim_df, aes(x = year, y = man_leader, group = topic, color = topic)) +
  geom_line() +
  theme(legend.position = "bottom", legend.title = NULL)+
  ylim(0,1)

## Leader: Woman to Man
ggplot(w2v_sim_df, aes(x = year, y = woman_to_man_leader, group = topic, color = topic)) +
  geom_line() +
  theme(legend.position = "bottom", legend.title = NULL)

## Mother: Woman
ggplot(w2v_sim_df, aes(x = year, y = woman_mother, group = topic, color = topic)) +
  geom_line() +
  theme(legend.position = "bottom", legend.title = NULL) +
  ylim(0.5,1)

## Father: Man
ggplot(w2v_sim_df, aes(x = year, y = man_father, group = topic, color = topic)) +
  geom_line() +
  theme(legend.position = "bottom", legend.title = NULL) +
  ylim(0.5,1)

## Mother-Father: Woman-Man
ggplot(w2v_sim_df, aes(x = year, y = woman_mother_to_man_father, group = topic, color = topic)) +
  geom_line() +
  theme(legend.position = "bottom", legend.title = NULL)

## Strong: Woman
ggplot(w2v_sim_df, aes(x = year, y = woman_strong, group = topic, color = topic)) +
  geom_line() +
  theme(legend.position = "bottom", legend.title = NULL)

## Strong: Man
ggplot(w2v_sim_df, aes(x = year, y = man_strong, group = topic, color = topic)) +
  geom_line() +
  theme(legend.position = "bottom", legend.title = NULL)

## Strong: Woman to Man
ggplot(w2v_sim_df, aes(x = year, y = woman_to_man_strong, group = topic, color = topic)) +
  geom_line() +
  theme(legend.position = "bottom", legend.title = NULL)

## Weak: Woman
ggplot(w2v_sim_df, aes(x = year, y = woman_weak, group = topic, color = topic)) +
  geom_line() +
  theme(legend.position = "bottom", legend.title = NULL) +
  ylim(-0.5,1)

## Weak: Man
ggplot(w2v_sim_df, aes(x = year, y = man_weak, group = topic, color = topic)) +
  geom_line() +
  theme(legend.position = "bottom", legend.title = NULL) +
  ylim(-0.5,1)

## Weak: Woman to Man
ggplot(w2v_sim_df, aes(x = year, y = woman_to_man_weak, group = topic, color = topic)) +
  geom_line() +
  theme(legend.position = "bottom", legend.title = NULL)