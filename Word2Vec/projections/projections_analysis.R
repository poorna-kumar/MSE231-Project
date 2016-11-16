library(tidyr)
library(dplyr)
library(ggplot2)
library(ggrepel)

w2v_df <- read.csv("projections.tsv", sep="\t")
curr_year <- 2006

gg_color_hue <- function(n) {
  hues = seq(15, 375, length = n + 1)
  hcl(h = hues, l = 65, c = 100)[1:n]
}

##########################
# PER YEAR - TOPIC WORDS #
##########################
cols <- gg_color_hue(5)

min_proj <- min(w2v_df$similarity)
max_proj <- max(w2v_df$similarity)

w2v_curr_df <- filter(w2v_df, year == curr_year, topic != 'neutral') %>%
                spread(key = word_diff, value = similarity)
names(w2v_curr_df)[c(4,5)] <- c("he_she","man_woman")
ggplot(w2v_curr_df, aes(x = he_she, y = man_woman, colour = topic)) +
  geom_point(size = .9) +
  geom_text_repel(aes(label = word), size = 3) +
  labs(x = "Cosine similarity with 'He' - 'She'", 
       y = "Cosine similarity with 'Man' - 'Woman'", 
       title = paste0("Year: ",curr_year)) +
  scale_colour_manual(name="",
                      values=cols,
                      breaks=c("arts","business","health","science&tech","service"),
                      labels=c("Arts", "Business", "Health", "Science & Technology", "Service")) +
  theme(legend.position = 'bottom') +
  xlim(min_proj,max_proj) + 
  ylim(min_proj,max_proj) 
ggsave(paste0("./Plots/Proj",curr_year,".png"), height = 5, width = 5)

#################
# NEUTRAL WORDS #
#################
w2v_curr_df <- filter(w2v_df, year == curr_year, topic == 'neutral') %>%
  spread(key = word_diff, value = similarity)
names(w2v_curr_df)[c(4,5)] <- c("he_she","man_woman")
ggplot(w2v_curr_df, aes(x = he_she, y = man_woman, colour = topic)) +
  geom_point(size = .9) +
  geom_text_repel(aes(label = word), size = 3) +
  labs(x = "Cosine similarity with 'He' - 'She'", 
       y = "Cosine similarity with 'Man' - 'Woman'", 
       title = paste0("Year: ",curr_year)) +
  theme(legend.position = "none") +
  xlim(min_proj,max_proj) + 
  ylim(min_proj,max_proj) 
ggsave(paste0("./Plots/ProjNeutral",curr_year,".png"), height = 5, width = 5)

#############
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