#lendo os dados
#dados processador i5
#data <- read.csv("data/result_i5.csv", header = TRUE, sep = ";")

#dados processador i7
#data <- read.csv("data/result_i5.csv", header = TRUE, sep = ";")

#dados processador xeon
data_xeon <- read.csv("data/output_xeon.csv", header = TRUE, sep = ";")

data_i5 <- read.csv("data/result_i5.csv", header = TRUE, sep = ";")

data_i7 <- read.csv("data/output_i7.csv", header = TRUE, sep = ";")

data_xeon$processador = "xeon"
data_i7$processador = " i7 "
data_i5$processador = " i5 "



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


data = rbind(data_i5,data_xeon,data_i7)

#fitting data to anova
aov <- lm(time~type + size ,data=data)
#aov_size <- lm(time~as.character(size),data=data)

anova_fun(aov, "type")


boxplot(time~type,data=data, main="Visão geral Tempo x Algoritmo", 
        xlab="Algoritmo", ylab="Tempo de execução")

boxplot(time~type,data=data[data$size == 1000,], main="Tempo x Algoritmo, Entrada 1000", 
        xlab="Algoritmo", ylab="Tempo de execução")

boxplot(time~type,data=data[data$size == 10000,], main="Tempo x Algoritmo, Entrada 1000", 
        xlab="Algoritmo", ylab="Tempo de execução")
