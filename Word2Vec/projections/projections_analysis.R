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

for (year_c in c(1987,2006)) {
  w2v_curr_df <- filter(w2v_df, year == year_c, topic != 'neutral' & topic != 'litcomp') %>%
                  spread(key = word_diff, value = similarity)
  names(w2v_curr_df)[c(4,5)] <- c("he_she","man_woman")
  ggplot(w2v_curr_df, aes(x = he_she, y = man_woman, colour = topic)) +
    geom_point(size = .9) +
    geom_text_repel(aes(label = word), size = 3) +
    labs(x = "Cosine similarity with 'He' - 'She'", 
         y = "Cosine similarity with 'Man' - 'Woman'") +
    scale_colour_manual(name="",
                        values=cols,
                        breaks=c("arts","business","health","science&tech","service"),
                        labels=c("Arts", "Business", "Health", "Science & Technology", "Service")) +
    theme(legend.position = 'bottom') +
    xlim(min_proj,max_proj) + 
    ylim(min_proj,max_proj) 
  ggsave(paste0("./Plots/Proj",year_c,".pdf"), height = 5, width = 5)
}

#################
# NEUTRAL WORDS #
#################
cols <- gg_color_hue(1)

w2v_curr_df <- filter(w2v_df, year == curr_year, topic == 'neutral') %>%
  spread(key = word_diff, value = similarity)
names(w2v_curr_df)[c(4,5)] <- c("he_she","man_woman")
ggplot(w2v_curr_df, aes(x = he_she, y = man_woman, colour = topic)) +
  geom_point(size = .9) +
  geom_text_repel(aes(label = word), size = 3) +
  labs(x = "Cosine similarity with 'He' - 'She'", 
       y = "Cosine similarity with 'Man' - 'Woman'") +
  scale_colour_manual(name="",
                      values=cols,
                      breaks=c("neutral"),
                      labels=c("Neutral")) +
  theme(legend.position = 'bottom') +
  xlim(min_proj,max_proj) + 
  ylim(min_proj,max_proj) 
ggsave(paste0("./Plots/ProjNeutral",curr_year,".pdf"), height = 5, width = 5)

#################
# COMPARISON WORDS #
#################
w2v_curr_df <- filter(w2v_df, year == curr_year, topic == 'litcomp') %>%
  spread(key = word_diff, value = similarity)
names(w2v_curr_df)[c(4,5)] <- c("he_she","man_woman")
ggplot(w2v_curr_df, aes(x = he_she, y = man_woman, colour = topic)) +
  geom_point(size = .9) +
  geom_text_repel(aes(label = word), size = 3) +
  labs(x = "Cosine similarity with 'He' - 'She'", 
       y = "Cosine similarity with 'Man' - 'Woman'") +
  theme(legend.position = "none") +
  xlim(min_proj,max_proj) + 
  ylim(min_proj,max_proj) 
ggsave(paste0("./Plots/ProjLitComp",curr_year,".pdf"), height = 5, width = 5)

######################
# OVER TIME - HE/SHE #
######################
cols <- gg_color_hue(5)
w2v_heshe_df <- filter(w2v_df, word_diff == "He-She" & topic != 'litcomp' & topic != 'neutral') %>% 
                  group_by(topic, year) %>%
                  summarise(avg_sim = mean(similarity))
ggplot(w2v_heshe_df, aes(x = year, y = avg_sim, colour = topic, group = topic)) + 
  geom_line() +
  scale_colour_manual(name="",
                      values=cols,
                      breaks=c("arts","business","health","science&tech","service"),
                      labels=c("Arts", "Business", "Health", "Science & Technology", "Service")) +
  labs(x = "", y = "Average Cosine Similarity to 'He'-'She'") +
  theme(legend.position = "none")
ggsave("./Plots/HeSheAvgOT.pdf", height = 5, width = 6)

######################
# OVER TIME - HE/SHE #
######################
w2v_manwoman_df <- filter(w2v_df, word_diff == "Man-Woman" & topic != 'litcomp' & topic != 'neutral') %>% 
  group_by(topic, year) %>%
  summarise(avg_sim = mean(similarity))
ggplot(w2v_manwoman_df, aes(x = year, y = avg_sim, colour = topic, group = topic)) + 
  geom_line() +
  scale_colour_manual(name="",
                      values=cols,
                      breaks=c("arts","business","health","science&tech","service"),
                      labels=c("Arts", "Business", "Health", "Science & Technology", "Service")) +
  labs(x = "", y = "Average Cosine Similarity to 'Man'-'Woman'") +
  theme(legend.position = "none")
ggsave("./Plots/ManWomanAvgOT.pdf", height = 5, width = 6)