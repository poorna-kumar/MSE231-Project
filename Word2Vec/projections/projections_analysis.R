library(tidyr)
library(dplyr)
library(ggplot2)
library(ggrepel)

w2v_df <- read.csv("projections.tsv", sep="\t")

# OVER TIME #
#############
words <- unique(w2v_df$word)
for (w in words) {
  w2v_word_df <- filter(w2v_df, word == w)
  ggplot(w2v_word_df, aes(x = year, y = similarity, colour = word_diff, group = word_diff)) +
               geom_line() +
               labs(x = "Year", y = "Similarity", colour = "Gendered Word", title = paste0("Word: ", w)) +
               theme(legend.position = 'bottom') +
               ylim(min(w2v_word_df$similarity)-0.05,max(w2v_word_df$similarity)+0.05)
  ggsave(paste0("./Plots/Word",w,"OT.png"))
}

# OVER TIME - AVG #
###################
w2v_avg_df <- group_by(w2v_df, year, topic, word_diff) %>%
                  summarise(avg_word_sim = mean(similarity))
topics <- unique(w2v_sim_df$topic)
for (t in topics) {
  w2v_topic_df <- filter(w2v_avg_df, topic == t)
  ggplot(w2v_topic_df, aes(x = year, y = avg_word_sim, colour = word_diff, group = word_diff)) +
          geom_line() +
          labs(x = "Year", y = "Similarity", colour = "Gendered Word", title = paste0("Topic: ", t)) +
          theme(legend.position = 'bottom') +
          ylim(min(w2v_topic_df$avg_word_sim)-0.05,max(w2v_topic_df$avg_word_sim)+0.05) 
  ggsave(paste0("./Plots/Topic",t,"OT.png"))
}