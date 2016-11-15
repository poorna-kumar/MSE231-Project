library(tidyr)
library(dplyr)
library(ggplot2)
library(ggrepel)

w2v_sim_df <- read.csv("all_similarities.tsv", sep="\t")

########################
# Pure Word Similarity #
########################
# BY YEAR #
###########
for (curr_year in 1987:2006) {
  # Man/Woman
  w2v_sim_mw_df <- filter(w2v_sim_df, year == curr_year & (gender_word == 'man' | gender_word == 'woman')) %>%
                        spread(key = gender_word, value = similarity)
  ggplot(w2v_sim_mw_df, aes(x = man, y = woman, colour = topic)) +
    geom_point(size = .9) +
    geom_text_repel(aes(label = word), size = 3) +
    labs(x = "Similarity with 'Man'", y = "Similarity with 'Woman'", title = paste0("Year: ",curr_year)) +
    theme(legend.position = 'bottom') +
    xlim(-0.25,.75) + 
    ylim(-0.25,.75) +
    geom_abline(intercept = 0, slope = 1)
  ggsave(paste0("./Plots/MW",curr_year,".png"))

  # He/She
  w2v_sim_hs_df <- filter(w2v_sim_df, year == curr_year & (gender_word == 'he' | gender_word == 'she')) %>%
                        spread(key = gender_word, value = similarity)
  ggplot(w2v_sim_hs_df, aes(x = he, y = she, colour = topic)) +
    geom_point(size = .9) +
    geom_text_repel(aes(label = word), size = 3) +
    labs(x = "Similarity with 'He'", y = "Similarity with 'She'", title = paste0("Year: ",curr_year)) +
    theme(legend.position = 'bottom') +
    xlim(-0.25,.75) + 
    ylim(-0.25,.75) +
    geom_abline(intercept = 0, slope = 1)
  ggsave(paste0("./Plots/HS",curr_year,".png"))
}

# OVER TIME #
#############
words <- unique(w2v_sim_df$word)
for (w in words) {
  w2v_sim_word_df <- filter(w2v_sim_df, word == w)
  ggplot(w2v_sim_word_df, aes(x = year, y = similarity, colour = gender_word, group = gender_word)) +
               geom_line() +
               labs(x = "Year", y = "Similarity", colour = "Gendered Word", title = paste0("Word: ", w)) +
               theme(legend.position = 'bottom') +
               ylim(min(w2v_sim_word_df$similarity)-0.05,max(w2v_sim_word_df$similarity)+0.05)
  ggsave(paste0("./Plots/Word",w,"OT.png"))
}

# OVER TIME - AVG #
###################
w2v_sim_avg_df <- group_by(w2v_sim_df, year, topic, gender_word) %>%
                  summarise(avg_word_sim = mean(similarity))
topics <- unique(w2v_sim_df$topic)
for (t in topics) {
  w2v_sim_topic_df <- filter(w2v_sim_avg_df, topic == t)
  ggplot(w2v_sim_topic_df, aes(x = year, y = avg_word_sim, colour = gender_word, group = gender_word)) +
          geom_line() +
          labs(x = "Year", y = "Similarity", colour = "Gendered Word", title = paste0("Topic: ", t)) +
          theme(legend.position = 'bottom') +
          ylim(min(w2v_sim_topic_df$avg_word_sim)-0.05,max(w2v_sim_topic_df$avg_word_sim)+0.05) 
  ggsave(paste0("./Plots/Topic",t,"OT.png"))
}