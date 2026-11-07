library(MASS)
x <- as.matrix(read.csv('profiles_independent.csv', header=FALSE)) / 1000
d <- dist(x)
write(order(d), 'native_order.txt', ncolumns=1)
z <- isoMDS(d)
colnames(z$points) <- c('x','y')
write.csv(z$points,'native_default.csv',row.names=FALSE)
cat(sprintf('Native all-default isoMDS stress: %.15g\n',z$stress))
w <- as.matrix(read.csv('evidence/witness.csv'))
s <- Shepard(d,w)
cat(sprintf('Native Shepard witness stress: %.15g\n',
            100*sqrt(sum((s$y-s$yf)^2)/sum(s$y^2))))
print(sessionInfo())
