#!/usr/bin/env Rscript
#This is a script that formats beavioral scan data into BIDS format
#henry.rossiter@utexas.edu

#import library("R.matlab") to read .mat files and suppress startup messages
suppressMessages(library("R.matlab"))

# run like - Rscript --vanilla BIDS_behavioral_formatter.R (first file path/name) (file output path/name)
# output should be a .tsv file to follow BIDS formatting rules
args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=TRUE)
}  
#if file read in is a .txt file
if (endsWith(args[1], "txt")){
	RAWdf <- read.table(args[1], header = TRUE)
	BIDdf <- data.frame(RAWdf$onset, RAWdf$duration, RAWdf$cond, RAWdf$answer, RAWdf$resp, RAWdf$RT)

	names(BIDdf) <- c("onset", "duration", "Trial_type", "answer", "Response", "Resp_time")

	#map integers in the Trial_type column to their corresponding trial type string
	nums=sort(unique(BIDdf$Trial_type))
	strings=c("face_match", "face_mismatch", "place_match", "place_mismatch")
	names(strings)=nums
	BIDdf$Trial_type=strings[BIDdf$Trial_type]

	#change answers- 1 stays at 1 and 0 becomes 2
	BIDdf$answer[BIDdf$answer == 0] <- 2
}
#if file read in is a .mat file
if (endsWith(args[1], "mat")){
	# method readMat returns list of lists
	matList <- readMat(args[1], header = TRUE)
	
	#bind together vectors : Onsets, Duration, Trial_type, Answer, Response, Response_time
	BIDdf <- data.frame(matList[[1]][[5]],matList[[1]][[10]],matList[[1]][[4]][1:126,2],matList[[1]][[4]][1:126,4],matList[[1]][[6]],matList[[1]][[7]])
	names(BIDdf) <- c('onset', 'duration', "Trial_type", "answer", "Response", "Resp_time")
	
	#round all float values to 1 decimal place
	is.num <- sapply(BIDdf, is.numeric)
	BIDdf[is.num] <- lapply(BIDdf[is.num], round, 1)
	
	#map integers in the Trial_type column to their corresponding trial type string
	nums=sort(unique(BIDdf$Trial_type))
	strings=c("face", "object", "scrambled object", "scene", "fixation cross")
	names(strings)=nums
	BIDdf$Trial_type=strings[BIDdf$Trial_type]
			

}
# change all "NA" values to "n/a"
BIDdf[is.na(BIDdf)] <- "n/a"

#write new .txt file and save to directory specified with second parameter
write.table(BIDdf, args[2], sep="\t", row.names = FALSE, quote = FALSE)
print(paste0("BIDS file saved to ", args[2]))
