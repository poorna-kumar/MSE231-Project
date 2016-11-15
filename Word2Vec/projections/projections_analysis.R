library(tidyr)
library(dplyr)
library(ggplot2)
library(ggrepel)

w2v_df <- read.csv("projections.tsv", sep="\t")

# PER YEAR #
############
min_proj <- min(w2v_df$similarity)
max_proj <- max(w2v_df$similarity)
for (curr_year in 1987:2006) {
  w2v_curr_df <- filter(w2v_df, year == curr_year) %>%
                  spread(key = word_diff, value = similarity)
  names(w2v_curr_df)[c(4,5)] <- c("he_she","man_woman")
  ggplot(w2v_curr_df, aes(x = he_she, y = man_woman, colour = topic)) +
    geom_point(size = .9) +
    geom_text_repel(aes(label = word), size = 3) +
    labs(x = "Cosine similarity with 'He' - 'She'", y = "Cosine similarity with 'Man' - 'Woman'", title = paste0("Year: ",curr_year)) +
    theme(legend.position = 'bottom') +
    xlim(min_proj,max_proj) + 
    ylim(min_proj,max_proj) 
  ggsave(paste0("./Plots/Proj",curr_year,".png"))
}

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
topics <- unique(w2v_df$topic)
for (t in topics) {
  w2v_topic_df <- filter(w2v_avg_df, topic == t)
  ggplot(w2v_topic_df, aes(x = year, y = avg_word_sim, colour = word_diff, group = word_diff)) +
          geom_line() +
          labs(x = "Year", y = "Similarity", colour = "Gendered Word", title = paste0("Topic: ", t)) +
          theme(legend.position = 'bottom') +
          ylim(min(w2v_topic_df$avg_word_sim)-0.05,max(w2v_topic_df$avg_word_sim)+0.05) 
  ggsave(paste0("./Plots/Topic",t,"OT.png"))
}