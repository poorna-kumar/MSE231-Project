library(tidyr)
library(dplyr)
library(ggplot2)
library(ggrepel)

w2v_sim_df <- read.csv("all_similarities.tsv", sep="\t")

########################
# Pure Word Similarity #
########################
for (curr_year in 1987:1994) {
  #
  # Man/Woman
  #
  w2v_sim_mw_df <- filter(w2v_sim_df, year == curr_year & (gender_word == 'man' | gender_word == 'woman')) %>%
                        spread(key = gender_word, value = similarity)
  print(ggplot(w2v_sim_mw_df, aes(x = man, y = woman, colour = topic)) +
    geom_point(size = .9) +
    geom_text_repel(aes(label = word), size = 3) +
    labs(x = "Similarity with 'Man'", y = "Similarity with 'Woman'", title = paste0("Year: ",curr_year)) +
    theme(legend.position = 'bottom') +
    xlim(-0.25,.75) + 
    ylim(-0.25,.75) +
    geom_abline(intercept = 0, slope = 1))

  #
  # He/She
  #    
  w2v_sim_hs_df <- filter(w2v_sim_df, year == curr_year & (gender_word == 'he' | gender_word == 'she')) %>%
                        spread(key = gender_word, value = similarity)
  print(ggplot(w2v_sim_hs_df, aes(x = he, y = she, colour = topic)) +
    geom_point(size = .9) +
    geom_text_repel(aes(label = word), size = 3) +
    labs(x = "Similarity with 'He'", y = "Similarity with 'She'", title = paste0("Year: ",curr_year)) +
    theme(legend.position = 'bottom') +
    xlim(-0.25,.75) + 
    ylim(-0.25,.75) +
    geom_abline(intercept = 0, slope = 1))
}