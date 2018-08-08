install.packages("ggplot2")
library(ggplot2)
setwd("~/Desktop")

data = read.csv("u20_mins.csv")

plot(data$Year, data$Minutes, xlab = "Year", ylab = "Total U20 Minutes", main="Average U20 American Minutes Played by Year per Team", pch=16, col=ifelse(x %% 2==0,"red","green"))

plot(data$Year, data$TotalMins, xlab = "Year", ylab = "Total U20 Minutes", main="Total U20 American Minutes Played by Year", pch=16, col=ifelse(data$TotalMins==2012,"blue","orange"))



gg <- ggplot(data, aes(x=Year, y=TotalMins, color=factor(Year %% 2)))
gg <- gg + geom_point(size=3)
gg <- gg + theme_bw()
gg <- gg + theme(legend.position="none") + ggtitle("Total U20 American Minutes") + theme(plot.title = element_text(hjust = 0.5))
gg


#Forgot about these graphs, which I think are way more fun to look at. They're U20 graphs, which is 1 year younger than thread eligible, but they're more revealing to me. This means to count this year you're a '98, last year you were a '97, etc.

#This is where you really see an improvement for playing time. I changed the colors to separate U20 WC years.
