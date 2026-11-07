# Here we analyse how a system of differential equations that describes tumor 
# growth and evolution behaves qualitatively. That is, whether it can 
# generate several stable equilibria or not. 
# 
# Author: Victor Garcia, ETH Zurich, July 2015
###############################################################################

library(rootSolve)

## =======================================================================
## Find the steady states 
## =======================================================================

### we solve the equations below, inspired from Conway and Perelson, 2013, PNAS, 
### with not mutation, and all of the saturation terms are consistent. 
### The extension to NK and CTL is inspired by de Pillis et al, 2005, cancer res
## Equations:
##  i)  dT_w/dt = T_w*(a*(1-b*T_w) - c*N*T_w -k*T_w*E 
##  ii) dN/dt = s_N -d_N*N + g*T_w*N/(h_g + T_w) - p*N*T_w/(h_p + T_w)
##  iii) dE/dt = -d_E*E + m*(E*T_w)/(h_m+T_w) - q*E*T_w/(h_q+T_w) +r*N*T_w


### define default parameters 
source("Rscripts/params_FengNKCTL.R")

### These are the equations we are fundamentally interested in, since adding mutation only 
### introduces escape. 

### The steady states are:
### NK cells 
# N* = -s_N/(g*T_w/(h_g + T_w) - p*T_w/(h_p + T_w) -d_N)

### This is the solution of the equlibrium of N of equation ii)
N.stab.nomut <- function(T_w, parameters){
	N.stimul = parameters$g*T_w/(parameters$hg + T_w^2)
	denominator = N.stimul - parameters$p*T_w/(parameters$hp + T_w) -parameters$dN
	N = -parameters$sN/denominator
	return(N)
}

### test 
N.stab.nomut(1E5, parameters)
x.lim = c(1, 1E9)

### test 
curve(N.stab.nomut(x, parameters), xlim = x.lim, log = "x", xlab = "T_w", ylab = "N*" ) 
abline(h = 0, col = "black")

### How does it behave under changes of parameters
parameters$p = 1E-1
parameters$g = 1E0
curve(N.stab.nomut(x, parameters), xlim = x.lim, log = "x", xlab = "T_w", ylab = "N*" ) 
abline(h = 0, col = "black")

### return to default parameters 
source("Rscripts/params_FengNKCTL.R")

### CTLs 
# E* = (-s_E*(h_q + T_w)*(h_m + T_w))/((m*T_w -d_E)*(h_q + T_w)-q*T_w*(h_m + T_w))

### This is the equlibrium solution of E as a function of T_w. 
### There are two branches of this solution. 
E.stab.nomut <- function(T_w, parameters){
	N = N.stab.nomut(T_w, parameters)
	Q = parameters$q*T_w/(parameters$hq + T_w)
	M = parameters$m*T_w/(parameters$hm + T_w)
	denominator = parameters$dE + Q - M
	return(parameters$r*N*T_w/denominator)
}

## test 
E.stab.nomut(0, parameters)
E.stab.nom

### original idea (not saturating exhaustion)
### first branch of solutions
y.lim = c(1,1E5)
curve(E.stab.nomut(x, parameters), col = "red", lwd =2,  xlim = x.lim, log = "x", xlab = "T_w", ylab = "E*") 
abline(h = 0, col = "black")

### lets play around withthe paramters a little bit
y.lim = c(1E1,1E5)
parameters$q = 0.099
curve(E.stab.nomut(x, parameters), col = "red", lwd =2, ylim = y.lim, xlim = x.lim, log = "x", xlab = "T_w", ylab = "E*") 
abline(h = 0, col = "black")


### return to default parameters 
source("Rscripts/params_FengNKCTL.R")

#####################################################################################

### To study the system, we implement the different terms appearing in i) to 
### obtain a feeling of how dT/dt behaves

#### Logistic growth Term 


### This is the logistic growth term in i)
loggrowth <- function(T_w, parameters){
	return(parameters$a*T_w*(1 - parameters$b*T_w) )
}

### how does it look with the parameters that we have?
curve(loggrowth(x, parameters), xlim = x.lim, log = "x", xlab = "T_w", ylab = "intrinsic growt rate tumor") 
abline(h = 0, col = "black")

### how a term -c*N*T_w would behave
curve(-parameters$c*N.stab.nomut(x, parameters)*x, xlim = x.lim, log = "x", xlab = "T_w", ylab = "N*") 

### Now we combine the two: #############

### combining log growth and the N

parameters$c = 1E-3
#parameters$p = 1E7
curve(loggrowth(x, parameters) - parameters$c*N.stab.nomut(x, parameters)*x, 
		xlim = x.lim, ylim = y.lim, 
		col = "violet", lwd = 2, 
		log = "x", xlab = "T_w", 
		ylab = "log.growth - NKkilling") 
abline(h = 0, col = "black")


### return to default parameters 
source("Rscripts/params_FengNKCTL.R")

### peer more deeply into what is happening: show only a window of -10, 10
curve(loggrowth(x, parameters) - parameters$c*N.stab.nomut(x, parameters)*x, 
		ylim = c(-10,10), xlim = x.lim, log = "x", 
		xlab = "T_w", ylab = "log.growth - NKkilling") 
abline(h = 0, col = "black")

### Playing around with parameters$c shows us, that we can obtain a stable and an unstable equlibrium 


### We keep on implementing CTL killing, and will see how this changes things
CTLkilling <- function(T_w, parameters){
	kill = parameters$k*E.stab.nomut(T_w, parameters)*T_w
	#kill = parameters$k*E.stab.nomut(T_w, parameters)*T_w
	return(kill)
}


### see how it behaves
curve( CTLkilling(x, parameters), col = "red", lwd =2, 
		ylim = y.lim, 
		xlim = x.lim, log = "x", 
		xlab = "T_w", ylab = "CTL killing") 
abline(h = 0, col = "black")


### and the killing efficacy?
parameters$k = 0.1
curve( CTLkilling(x, parameters), col = "red", lwd =2, ylim = y.lim, xlim = x.lim, log = "x", xlab = "T_w", ylab = "CTL killing") 
abline(h = 0, col = "black")


### return to default parameters 
source("Rscripts/params_FengNKCTL.R")

### Let us combine the CTL killing and the cancer growth stimulation
parameters$k = 1E1
y.lim = c(-1E6, 1E6)

########################################################
##### And now the saturating version

### return to default parameters 
source("Rscripts/params_FengNKCTL.R")


pdf("dTdt_FengNKCTL.pdf")
   limit = 5E7
   y.lim = c(-limit, limit)
   x.lim = c(1, 1E9)
   
   parameters$c = 5E-4
   parameters$k = 1E-4
   
   #### logistic growth 
   curve(loggrowth(x, parameters) , 
   		xlim = x.lim, ylim = y.lim,
   		col = "green", lwd = 2, 
   		log = "x", xlab = "T_w", 
   		ylab = "") 
   abline(h = 0, col = "black")
   
   
   #### NK killing
   par(new = TRUE)
   curve(-parameters$c*N.stab.nomut(x, parameters)*x, 
   		xlim = x.lim, ylim = y.lim,
   		col = "lightblue", lwd = 2, 
   		log = "x", xlab = "T_w", 
   		ylab = "") 
   abline(h = 0, col = "black")
   
   ### combined logistic growth with NK killing
   par(new = TRUE)
   curve(loggrowth(x, parameters) - parameters$c*N.stab.nomut(x, parameters)*x, 
   		xlim = x.lim, ylim = y.lim, 
   		col = "violet", lwd = 2, 
   		log = "x", xlab = "T_w", 
   		ylab = "log.growth - NKkilling") 
   abline(h = 0, col = "black")
   
   
   #### CTL killing
   
   
   par(new = TRUE)
   curve(loggrowth(x, parameters) 
   				- parameters$c*N.stab.nomut(x, parameters)*x 
   				-CTLkilling(x, parameters),  
   		xlim = x.lim, ylim = y.lim,
   		col = "blue", lwd = 2, 
   		log = "x", 
   		ylab = "dT/dt(T)", 
   		xlab = "T_w") 
   abline(h = 0, col = "black")
   
dev.off()

write.table(file = "plots/parameters_dTdt_FengNKCT.txt", parameters)



### Inserting the solutions of E and N into i), we obtain a function of dT/dt. 
### the nullcline of this equation (points) are the steady states of the 
### system. The stable steady states show increasing dT/dt for smaller T values, 
### and the opposite for larger T values

### Now we plug the solutions of ii) and iii) into i), to obtain 
### an expression for dT_w/dt(T_w), which can then be further analysed for 
### its roots
dTdt.nomut = function(T_w, parameters){
	### retrieve solutions from before
	E.stable = E.stab.nomut(T_w, parameters)
	N.stable = N.stab.nomut(T_w, parameters)
	
	### go through terms: logistict growt
	log.growth = parameters$a*T_w*(1 - parameters$b*T_w)
	### NK killing 
	NKkill = -parameters$c*N.stable*T_w
	### CTL killing 
	CTLkill = -parameters$k*E.stable*T_w
	
	return(log.growth + NKkill + CTLkill)
}


### test
limit = 5E7
y.lim = c(-limit, limit)
x.lim = c(1, 1E9)

curve(dTdt.nomut(x, parameters), 
		xlim = x.lim, ylim = y.lim, 
		lwd = 3, col = "magenta", 
		log = "x", xlab = "T_w", 
		ylab = "dT/dt") 
abline(h = 0, col = "black")

### play around with parameters
parameters$k = 1E0
parameters$c = 1E-4
parameters$hk = 5


y.lim = c(-1E5, 1E5)
curve(dTdt.nomut(x, parameters), xlim = x.lim, ylim = y.lim, 
		log = "x", xlab = "T_w", ylab = "dT/dt", lwd = 3) 
abline(h = 0, col = "black")

### return to default parameters 
source("Rscripts/params_FengNKCTL.R")


########################################################################################
######## find steady states in numerically #############################################
########################################################################################


### Now we plug the solutions of ii) and iii) into i), to obtain 
### an expression for dT_w/dt(T_w), which can then be further analysed for 
### its roots
dTdt.nomut.log = function(log10.T_w, parameters){
	
	### reconvert 
	T_w = 10^log10.T_w
	
	### retrieve solutions from before
	E.stable = E.stab.nomut(T_w, parameters)
	N.stable = N.stab.nomut(T_w, parameters)
	
	### go through terms: logistict growt
	log.growth = parameters$a*T_w*(1 - parameters$b*T_w)
	### NK killing 
	NKkill = -parameters$c*N.stable*T_w
	### CTL killing 
	CTLkill = -parameters$k*E.stable*T_w
	
	return(log.growth + NKkill + CTLkill)
}


### search algorithm for the roots of equilibrium.det.log
steady.states.T.nomut <- function(parameters, interval = c(-1,12), maxiter = 3000){
	
	roots <- uniroot.all(function(x) dTdt.nomut.log(x, parameters), interval = interval, maxiter = maxiter)
	roots <- 10^roots
	
	### T == 0 is always a root!
	roots <- c(0, roots)
	
	return(roots)
}


### test 
#steady.states.T.nomut(parameters)
### works


### This is an auxiliary function that allows to 
### modify a list of parameters called "parameters"
### by passing a named vector mod.par.vals. 
### The entry names of mod.par.vals determine 
### which parameter entries are going to be replaced, 
### and the values determine with what values the 
### parameter entries are going to be replaced with. 
mod.params <- function(parameters, mod.par.vals){
	
	par.names <- names(parameters)
	for(i in 1:length(mod.par.vals)){
		repl.ind <- which(names(parameters) == names(mod.par.vals)[i])
		parameters[[repl.ind]] <- mod.par.vals[i]
	}
	
	names(parameters) = par.names
	
	return(parameters)
}



#######################################################################################################
### Plot dependency of rate of change of T_w on T_w itself (geometrical stability analysis) ###########
#######################################################################################################
### return to default parameters 
source("Rscripts/params_FengNKCTL.R")

parameters$c = 1E-3
parameters$k = 1E-5

pdf(file = "plots/dTdt_FengNKCTL_c_dependency.pdf", 
		width = 12, height = 5)

   x.lim = c(1, 1E10)
   limit = 5E7
   y.lim = c(-limit, limit)
   
   cex = 2
   
   par(oma = c(2,7,1,1))
   par(mfrow = c(1,3))
   
   ### low c 
   parameters$c = 1E-7
   curve(dTdt.nomut(x, parameters), 
   		xlim = x.lim, ylim = y.lim, 
   		lwd = 3, col = "blue", 
   		log = "x", xlab = "", 
   		ylab = "", axes = F) 
   
   abline(h = 0, col = "black")
   
   roots <- steady.states.T.nomut(parameters)
   points(roots, rep(0, length(roots)), col = "blue", cex = cex, lwd = cex)
   
   
   ### tickers and labels at the tickers with exponents and axes
   exponent.x <- seq(from = log10(min(x.lim)), to = log10(max(x.lim)), by = 2)
   legend.expr.x <- as.expression(sapply(exponent.x, function(x) bquote(10^.(x)) ))
   
   #exponent.y <- seq(from = log10(1), to = log10(max(y.lim)), by = 2)
   tickers <- seq(from = 0, to = max(y.lim), by = max(y.lim)/2)[-1]
   exponent.y <- floor(log10(tickers))
   bases = tickers/10^floor(log10(tickers))
   
   #legend.expr.y <- as.expression(sapply(exponent.y, function(x) bquote(10^.(x)) ))
   legend.expr.y <- as.expression(sapply(1:length(bases), function(x) bquote(.(bases[x]) %.% 10^.(exponent.y[x])) ))
   legend.expr.y.rev <- as.expression(sapply(1:length(bases), function(x) bquote(-.(bases[x]) %.% 10^.(exponent.y[x])) ))
   
   tickers <- c(-rev(tickers), 0, tickers)
   exponent.y2 <- c(rev(exponent.y), 0, exponent.y)
   legend.expr.y <- c(rev(legend.expr.y.rev), as.expression(0), legend.expr.y)
   
   
   axis(1, at = 10^exponent.x, label = legend.expr.x, mgp = c(3,1.5,0), cex.axis = cex)
   #axis(2, las =1, cex.axis = cex)
   axis(2, at = tickers, label = legend.expr.y, las = 1, cex.axis = cex)
   
   #### axis labels
   #mtext(expression(paste("tumor size [",cells,"]", sep = "")), side=1, outer=F, line= 5, cex = cex)
   mtext(expression(paste("rate of change in tumor size [",cells %.% day^-1,"]", sep = "")), 
   		side=2, outer=F, line= 7.5, cex = 0.75*cex)
   
   #### middle c 
   parameters$c = 1E-3
   curve(dTdt.nomut(x, parameters), 
   		xlim = x.lim, ylim = y.lim, 
   		lwd = 3, col = "blue", 
   		log = "x", xlab = "", 
   		ylab = "", axes = F) 
   
   abline(h = 0, col = "black")
   
   roots <- steady.states.T.nomut(parameters)
   points(roots, rep(0, length(roots)), col = "blue", cex = cex, lwd = cex)
   
   
   ### tickers and labels at the tickers with exponents and axes
   exponent.x <- seq(from = log10(min(x.lim)), to = log10(max(x.lim)), by = 2)
   legend.expr.x <- as.expression(sapply(exponent.x, function(x) bquote(10^.(x)) ))
   
   #exponent.y <- seq(from = log10(1), to = log10(max(y.lim)), by = 2)
   tickers <- seq(from = 0, to = max(y.lim), by = max(y.lim)/2)[-1]
   exponent.y <- floor(log10(tickers))
   bases = tickers/10^floor(log10(tickers))
   
   #legend.expr.y <- as.expression(sapply(exponent.y, function(x) bquote(10^.(x)) ))
   legend.expr.y <- as.expression(sapply(1:length(bases), function(x) bquote(.(bases[x]) %.% 10^.(exponent.y[x])) ))
   legend.expr.y.rev <- as.expression(sapply(1:length(bases), function(x) bquote(-.(bases[x]) %.% 10^.(exponent.y[x])) ))
   
   
   tickers <- c(-rev(tickers), 0, tickers)
   exponent.y2 <- c(rev(exponent.y), 0, exponent.y)
   legend.expr.y <- c(rev(legend.expr.y.rev), as.expression(0), legend.expr.y)
   
   
   axis(1, at = 10^exponent.x, label = legend.expr.x, mgp = c(3,1.5,0), cex.axis = cex)
   #axis(2, las =1, cex.axis = cex)
   axis(2, at = tickers, label = legend.expr.y, las = 1, cex.axis = cex)
   
   #### axis labels
   mtext(expression(paste("tumor size [",cells,"]", sep = "")), 
   		side=1, outer=F, line= 5, cex = 0.75*cex)
   
   
   #### high c
   parameters$c = 1E0
   curve(dTdt.nomut(x, parameters), 
   		xlim = x.lim, ylim = y.lim, 
   		lwd = 3, col = "blue", 
   		log = "x", xlab = "", 
   		ylab = "", axes = F) 
   
   abline(h = 0, col = "black")
   
   roots <- steady.states.T.nomut(parameters)
   points(roots, rep(0, length(roots)), col = "blue", cex = cex, lwd = cex)
   
   
   ### tickers and labels at the tickers with exponents and axes
   exponent.x <- seq(from = log10(min(x.lim)), to = log10(max(x.lim)), by = 2)
   legend.expr.x <- as.expression(sapply(exponent.x, function(x) bquote(10^.(x)) ))
   
   #exponent.y <- seq(from = log10(1), to = log10(max(y.lim)), by = 2)
   tickers <- seq(from = 0, to = max(y.lim), by = max(y.lim)/2)[-1]
   exponent.y <- floor(log10(tickers))
   bases = tickers/10^floor(log10(tickers))
   
   #legend.expr.y <- as.expression(sapply(exponent.y, function(x) bquote(10^.(x)) ))
   legend.expr.y <- as.expression(sapply(1:length(bases), function(x) bquote(.(bases[x]) %.% 10^.(exponent.y[x])) ))
   legend.expr.y.rev <- as.expression(sapply(1:length(bases), function(x) bquote(-.(bases[x]) %.% 10^.(exponent.y[x])) ))
   
   
   tickers <- c(-rev(tickers), 0, tickers)
   exponent.y2 <- c(rev(exponent.y), 0, exponent.y)
   legend.expr.y <- c(rev(legend.expr.y.rev), as.expression(0), legend.expr.y)
   
   
   axis(1, at = 10^exponent.x, label = legend.expr.x, mgp = c(3,1.5,0), cex.axis = cex)
   #axis(2, las =1, cex.axis = cex)
   axis(2, at = tickers, label = legend.expr.y, las = 1, cex.axis = cex)
   

dev.off()

### store the parameters with which this plot was produced. 
### ATTENTION!!! the parameter names in the manuscript do not correspond 
### to the parameter names in the script.
write.table(file = "plots/parameters_dTdt_FengNKCT_c_dependency.txt", parameters)


#outcome <- cancer.massact.mdl(parameters= parameters,verbose = TRUE)
#plot_data(outcome)

########################################################################################
######## bifurcation plots #############################################
########################################################################################

### test of mod.params
source("Rscripts/params_FengNKCTL.R")

#mod.params(parameters, mod.par.vals = c("c" = 1E-10))
#mod.params(parameters, mod.par.vals = list(c = 1E-10))

parameters$c = 1E-3
parameters$k = 1E-5

### show how the solutions of the system bifurcate when varying one parameter value
bifurcation.plot <- function(parameters, x.lim = c(1E-8,1E0), log.plot = FALSE, cex = 2, stepsize = 0.005){
	
   if(log.plot){
      pdf("plots/bifurcation_c_FengNKCTL.pdf", width = 7, height = 6)
   }
	else{
	   pdf("plots/bifurcation_c_FengNKCTL_log.pdf", width = 7, height = 6)
	}
	
	par(oma = c(2,7,1,1))
	
   
	y.lim = c(0,1)
   if(log.plot){
      y.lim = c(1E-10,1)
   }
	
	### tickers and labels at the tickers with exponents and axes
	exp.x <- seq(from = log10(min(x.lim)), to = log10(max(x.lim)), by = stepsize)
	
	#parameters <-  mod.params(parameters, list(c = 10^x))
	### interval is where we search in T_w space
	roots <- lapply(exp.x, function(x) steady.states.T.nomut( mod.params(parameters, c("c" = 10^x)), interval = c(-1,12) ) )
	
	#plot(10^exp.x, roots[1], col = "blue", type = "l")
	
	col.code <- function(vec.length, ref.root = 1){
		
		modifier = ref.root - 1
		if(vec.length == 1 + modifier){
			return("blue")
		} 
		if(vec.length == 2 + modifier){
			return("red")
		} 
		if(vec.length == 3 + modifier){
			return("blue")
		} 
		if(vec.length == 4 + modifier){
			return("red")
		} 
		
		if(ref.root > vec.length){
			return("green")
		}
	}
	
   
	if(log.plot){
	   plot(x.lim[1],0,type = "n", 
	        xlim = x.lim, ylim = y.lim, 
	        log = "xy", main = "", 
	        xlab = "", ylab = "", 
	        axes = F) 
	}
   else{
      plot(x.lim[1],0,type = "n", 
           xlim = x.lim, ylim = y.lim, 
           log = "x", main = "", 
           xlab = "", ylab = "", 
           axes = F) 
   }

	#sapply(1:length(exp.x), 
	#		function(x) if(length(roots[[x]])> 0){ for(i in 1:length(roots[[x]])){ points(10^exp.x[x],parameters$b*roots[[x]][i], type = "b", col = "blue", lwd = 1) } })
	
	
	n.vec = 1:length(exp.x)
	root.lengths <- sapply(n.vec,function(x) length(roots[[x]]))
	
	### number 1
	max.len <- max(root.lengths)
	
	for(i in 1:max.len){
		root.vals <- sapply(n.vec, function(x) parameters$b*roots[[x]][i])
		colrs = sapply(n.vec, function(x) col.code(root.lengths[x], ref.root = i))
		#print(cols)
		
		unique.cols = unique(colrs)
		nmb.col = length(unique.cols)
		
		for(j in 1:nmb.col){
			col.ind = which(colrs == unique.cols[j])
			lines((10^exp.x)[col.ind], root.vals[col.ind], col = unique.cols[j], lwd = 3)
		}
	}
	
	exponent.x <- seq(from = log10(min(x.lim)), to = log10(max(x.lim)), by = 2)
	legend.expr.x <- as.expression(sapply(exponent.x, function(x) bquote(10^.(x)) ))
	
	
	#exponent.y <- seq(from = log10(1), to = log10(max(y.lim)), by = 2)
	tickers <- seq(from = 0, to = max(y.lim), by = max(y.lim)/4)[-1]
	exponent.y <- floor(log10(tickers))
	bases = tickers/10^floor(log10(tickers))
	
	#legend.expr.y <- as.expression(sapply(exponent.y, function(x) bquote(10^.(x)) ))
	legend.expr.y <- as.expression(sapply(1:length(bases), function(x) bquote(.(bases[x]) %.% 10^.(exponent.y[x])) ))
	
	tickers <- c( 0, tickers)
	exponent.y2 <- c( 0, exponent.y)
	legend.expr.y <- c(as.expression(0), legend.expr.y)
	
	
	axis(1, at = 10^exponent.x, label = legend.expr.x, mgp = c(3,1.5,0), cex.axis = cex)
	axis(2, las =1, cex.axis = cex)
	#axis(2, at = tickers, label = legend.expr.y, las = 1, cex.axis = cex)
	
	
	#### axis labels
	mtext(expression(paste("c [",cells %.% day^-1,"]", sep = "")), 
			side=1, outer=F, line= 4, cex = cex)
	mtext(expression(paste("relative tumor burden bT", sep = "")), 
			side=2, outer=F, line= 8, cex = cex)
	
	dev.off()
}

bifurcation.plot(parameters, log.plot = FALSE)

### store the parameters with which this figure was produced
write.table(file = "plots/parameters_bifurcation_c_FengNKCT.txt", parameters)



#########################################################################################
####  A bigger figure to see how the dynamics of the system develop with the parameter values 
#########################################################################################

source("Rscripts/params_FengNKCTL.R")
#parameters$c = 1E-3
#parameters$s = 2E1


#### For this to work, we must have defined a script called stoch_cancer_model_FengNKCTL.R 
### which ought to be called before running it. The script contains the code to simulate 
### the dyamics of the set of equations defined above, at the beginning of THIS script, 
### in a stochastic as well as in a deterministic fashion. 

source("Rscripts/stoch_cancer_model_FengNKCTL.R")

pdf(file = "plots/dynamics_dTdt_FengNKCTL_c_dependency.pdf", 
		width = 12, height = 5)
   
   x.lim = c(1, 1E10)
   limit = 5E7
   y.lim = c(-limit, limit)
   
   cex = 2
   
   par(oma = c(2,7,1,1))
   par(mfrow = c(2,3))
   
   #########################################################################################
   ### try to understand what is not working here
   init = c(T_w= 100,T_m=0,NK=parameters$sN/parameters$dN,EFF=0)
   state = init
   init = c(T_w= 100,T_m=0,NK=0,EFF=0)
   state = init
   parms = parameters
   with(as.list(c(state, parms)),{
   			dT_w <- a*T_w*(1-b*(T_w+T_m)) - c*NK*T_w -k*EFF*T_w + s*EFF*T_w - mu*T_w
   			dT_m <- mu*T_w + a*T_m*(1-b*(T_w+T_m)) 
   			dNK <- sN - dN*NK + g*T_w*NK - p*NK*T_w
   			dEFF <- sE - dE*EFF + m*EFF*T_w - q*EFF*T_w + r*NK*T_w
   			if(verbose){
   				cat(paste(c(dT_w, dT_m, dNK, dEFF), collapse =";"), '\n')
   			}
   			list(c(dT_w,dT_m,dNK,dEFF))
   		})
   
   init = c(T_w= 100,T_m=0,NK=10,EFF=1)
   state = init
   
   #########################################################################################�
   
   ### low c 
   parameters$c = 1E-7
   outcome <- cancer.massact.mdl(init = init, 
   		parameters= parameters,verbose = TRUE,
   		times=seq(0, 30, length=1000), method = "ode45")
   plot_data(outcome)
   
   
   ### middle c 
   parameters$c = 1E-3
   outcome <- cancer.massact.mdl(init = init,parameters= parameters,verbose = TRUE)
   plot_data(outcome)
   
   ### high c 
   parameters$c = 1E-2
   outcome <- cancer.massact.mdl(init = init, parameters= parameters,verbose = TRUE)
   plot_data(outcome)
   
   
   ### low c 
   parameters$c = 1E-7
   curve(dTdt.nomut(x, parameters), 
   		xlim = x.lim, ylim = y.lim, 
   		lwd = 3, col = "blue", 
   		log = "x", xlab = "", 
   		ylab = "", axes = F) 
   
   abline(h = 0, col = "black")
   
   roots <- steady.states.T.nomut(parameters)
   points(roots, rep(0, length(roots)), col = "blue", cex = cex, lwd = cex)
   
   
   ### tickers and labels at the tickers with exponents and axes
   exponent.x <- seq(from = log10(min(x.lim)), to = log10(max(x.lim)), by = 2)
   legend.expr.x <- as.expression(sapply(exponent.x, function(x) bquote(10^.(x)) ))
   
   #exponent.y <- seq(from = log10(1), to = log10(max(y.lim)), by = 2)
   tickers <- seq(from = 0, to = max(y.lim), by = max(y.lim)/2)[-1]
   exponent.y <- floor(log10(tickers))
   bases = tickers/10^floor(log10(tickers))
   
   #legend.expr.y <- as.expression(sapply(exponent.y, function(x) bquote(10^.(x)) ))
   legend.expr.y <- as.expression(sapply(1:length(bases), function(x) bquote(.(bases[x]) %.% 10^.(exponent.y[x])) ))
   legend.expr.y.rev <- as.expression(sapply(1:length(bases), function(x) bquote(-.(bases[x]) %.% 10^.(exponent.y[x])) ))
   
   tickers <- c(-rev(tickers), 0, tickers)
   exponent.y2 <- c(rev(exponent.y), 0, exponent.y)
   legend.expr.y <- c(rev(legend.expr.y.rev), as.expression(0), legend.expr.y)
   
   
   axis(1, at = 10^exponent.x, label = legend.expr.x, mgp = c(3,1.5,0), cex.axis = cex)
   #axis(2, las =1, cex.axis = cex)
   axis(2, at = tickers, label = legend.expr.y, las = 1, cex.axis = cex)
   
   #### axis labels
   #mtext(expression(paste("tumor size [",cells,"]", sep = "")), side=1, outer=F, line= 5, cex = cex)
   mtext(expression(paste("rate of change in tumor size [",cells %.% day^-1,"]", sep = "")), 
   		side=2, outer=F, line= 7, cex = 0.75*cex)
   
   #### middle c 
   parameters$c = 1E-3
   curve(dTdt.nomut(x, parameters), 
   		xlim = x.lim, ylim = y.lim, 
   		lwd = 3, col = "blue", 
   		log = "x", xlab = "", 
   		ylab = "", axes = F) 
   
   abline(h = 0, col = "black")
   
   roots <- steady.states.T.nomut(parameters)
   points(roots, rep(0, length(roots)), col = "blue", cex = cex, lwd = cex)
   
   
   ### tickers and labels at the tickers with exponents and axes
   exponent.x <- seq(from = log10(min(x.lim)), to = log10(max(x.lim)), by = 2)
   legend.expr.x <- as.expression(sapply(exponent.x, function(x) bquote(10^.(x)) ))
   
   #exponent.y <- seq(from = log10(1), to = log10(max(y.lim)), by = 2)
   tickers <- seq(from = 0, to = max(y.lim), by = max(y.lim)/2)[-1]
   exponent.y <- floor(log10(tickers))
   bases = tickers/10^floor(log10(tickers))
   
   #legend.expr.y <- as.expression(sapply(exponent.y, function(x) bquote(10^.(x)) ))
   legend.expr.y <- as.expression(sapply(1:length(bases), function(x) bquote(.(bases[x]) %.% 10^.(exponent.y[x])) ))
   legend.expr.y.rev <- as.expression(sapply(1:length(bases), function(x) bquote(-.(bases[x]) %.% 10^.(exponent.y[x])) ))
   
   
   tickers <- c(-rev(tickers), 0, tickers)
   exponent.y2 <- c(rev(exponent.y), 0, exponent.y)
   legend.expr.y <- c(rev(legend.expr.y.rev), as.expression(0), legend.expr.y)
   
   
   axis(1, at = 10^exponent.x, label = legend.expr.x, mgp = c(3,1.5,0), cex.axis = cex)
   #axis(2, las =1, cex.axis = cex)
   axis(2, at = tickers, label = legend.expr.y, las = 1, cex.axis = cex)
   
   #### axis labels
   mtext(expression(paste("tumor size [",cells,"]", sep = "")), 
   		side=1, outer=F, line= 5, cex = 0.75*cex)
   
   
   #### high c
   parameters$c = 1E0
   curve(dTdt.nomut(x, parameters), 
   		xlim = x.lim, ylim = y.lim, 
   		lwd = 3, col = "blue", 
   		log = "x", xlab = "", 
   		ylab = "", axes = F) 
   
   abline(h = 0, col = "black")
   
   roots <- steady.states.T.nomut(parameters)
   points(roots, rep(0, length(roots)), col = "blue", cex = cex, lwd = cex)
   
   
   ### tickers and labels at the tickers with exponents and axes
   exponent.x <- seq(from = log10(min(x.lim)), to = log10(max(x.lim)), by = 2)
   legend.expr.x <- as.expression(sapply(exponent.x, function(x) bquote(10^.(x)) ))
   
   #exponent.y <- seq(from = log10(1), to = log10(max(y.lim)), by = 2)
   tickers <- seq(from = 0, to = max(y.lim), by = max(y.lim)/2)[-1]
   exponent.y <- floor(log10(tickers))
   bases = tickers/10^floor(log10(tickers))
   
   #legend.expr.y <- as.expression(sapply(exponent.y, function(x) bquote(10^.(x)) ))
   legend.expr.y <- as.expression(sapply(1:length(bases), function(x) bquote(.(bases[x]) %.% 10^.(exponent.y[x])) ))
   legend.expr.y.rev <- as.expression(sapply(1:length(bases), function(x) bquote(-.(bases[x]) %.% 10^.(exponent.y[x])) ))
   
   
   tickers <- c(-rev(tickers), 0, tickers)
   exponent.y2 <- c(rev(exponent.y), 0, exponent.y)
   legend.expr.y <- c(rev(legend.expr.y.rev), as.expression(0), legend.expr.y)
   
   
   axis(1, at = 10^exponent.x, label = legend.expr.x, mgp = c(3,1.5,0), cex.axis = cex)
   #axis(2, las =1, cex.axis = cex)
   axis(2, at = tickers, label = legend.expr.y, las = 1, cex.axis = cex)
   

dev.off()


