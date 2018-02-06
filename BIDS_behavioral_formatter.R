#!/usr/bin/env Rscript
#This is a script that formats beavioral data into BIDS format
#henry.rossiter@utexas.edu

# run like - Rscript --vanilla BIDS_behavioral_formatter.R (first file path/name) (file output path/name)
args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=TRUE)
}  
RAWdf <- read.table(args[1], header = TRUE)
BIDdf <- data.frame(RAWdf$onset, RAWdf$duration, RAWdf$cond, RAWdf$answer, RAWdf$resp, RAWdf$RT)

names(BIDdf) <- c("Onsets", "Duration", "Trial_type", "answer", "Response", "Resp_time")

#map integers in the Trial_type column to their corresponding trial type string
nums=sort(unique(BIDdf$Trial_type))
strings=c("face_match", "face_mismatch", "place_match", "place_mismatch")
names(strings)=nums
BIDdf$Trial_type=strings[BIDdf$Trial_type]

#change answers- 1 stays at 1 and 0 becomes 2
BIDdf$answer[BIDdf$answer == 0] <- 2

#write new .txt file and save to directory specified with second parameter
write.table(BIDdf, args[2], sep="\t", row.names = FALSE)
print(paste0("BIDS file saved to ", args[2]))