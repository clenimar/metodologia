#lendo os dados
#dados processador i5
data <- read.csv("data/result_i5.csv", header = TRUE, sep = ";")

#dados processador i7
#data <- read.csv("data/result_i5.csv", header = TRUE, sep = ";")

#dados processador xeon
#data <- read.csv("data/result_i5.csv", header = TRUE, sep = ";")

anova_fun <- function(analysis, type){
  
  #anova
  #H0: os algoritmos sao iguais
  #H1: os algoritmos nao sao iguais (p<0.05) 
  anova <- aov(analysis)
  
  file_name <- " anova sumary.txt"
  file_name <- paste(type, file_name)
  s <- summary(anova)
  capture.output(s, file = file_name)
  
  name <- " plot witch 1.png"
  name <- paste(type, name)
  png(filename=name)
  #Caso queira visualizar o gráfico
  plot(analysis, which = 1)
  dev.off()
  
  name <- " plot witch 2.png"
  name <- paste(type, name)
  png(filename=name)
  #can se that there's a positive skewness in the data
  plot(analysis, which = 2)
  dev.off()
  
  sresids <- rstandard(analysis)
  
  name <- " histogram.png"
  name <- paste(type, name)
  png(filename=name)
  hist(sresids)
  dev.off()
  
}

name <- " type stripchart.png"
png(filename=name)

#visualizing data
stripchart(time~type,
           data=data,
           main="Different strip chart for each type",
           xlab="Type",
           ylab="Time",
           col="brown3",
           vertical=TRUE,
           pch=19,
           method = "jitter", jitter = 0.004
)
dev.off()

name <- " size stripchart.png"
png(filename=name)
stripchart(time~as.character(size),
           data=data,
           main="Different strip chart for each type",
           xlab="Type",
           ylab="Time",
           col="brown3",
           vertical=TRUE,
           pch=19,
           method = "jitter", jitter = 0.004
)
dev.off()



#fitting data to anova
aov_type <- lm(time~type,data=data)
aov_size <- lm(time~as.character(size),data=data)

anova_fun(aov_type, "type")
anova_fun(aov_size, "size")

