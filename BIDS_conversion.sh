#BIDS Conversion Script for UT Cognitive Neuroscience Lab's Aging Study
#accesses data from server, converts to BIDS form, and saves to server

export WORKING_DIR=/Volumes/schnyer/Aging_DecMem
export SOURCE_DIR=$WORKING_DIR/Scan_Data/Behavioral
export BIDS_DIR=$WORKING_DIR/Scan_Data/BIDS
export RSCRIPTPATH=$WORKING_DIR/Scan_Data/Behavioral

##Choose Participant
echo '\n'
echo "Which participant?"
read PARTIC

##Find behavioral directories
MEM_BEHAVIORAL=$SOURCE_DIR/$PARTIC/Memory
echo "Attempting to access behavioral data files in: " $MEM_BEHAVIORAL

##Create BIDS filenames
MEM_BehavioralMatch1_FILE="sub-"$PARTIC""_task-MemMatch_run-01_events
MEM_BehavioralRepeat1_FILE="sub-"$PARTIC""_task-MemRepeat_run-01_events
MEM_BehavioralMatch2_FILE="sub-"$PARTIC""_task-MemMatch_run-02_events
MEM_BehavioralRepeat2_FILE="sub-"$PARTIC""_task-MemRepeat_run-02_events
MEM_BehavioralMatch3_FILE="sub-"$PARTIC""_task-MemMatch_run-03_events
MEM_BehavioralRepeat3_FILE="sub-"$PARTIC""_task-MemRepeat_run-03_events

##Create BID formatted behavioral directory
if [ ! -d $BIDS_DIR/"sub-"$PARTIC""/func ]; then
    mkdir -p $BIDS_DIR/"sub-"$PARTIC""/func
fi

##Convert Files to BIDS Format
#calls R-script named BIDS_behavioral_formatter.R for each file
if [ ! -z "$MEM_BEHAVIORAL" ]; then
    for filename in "$MEM_BEHAVIORAL"/*; do
    	if [[ $filename = *"match_run1"* ]] &&  [[ $filename = *".txt" ]] ; then
  			echo "found raw data for task match 1. Attempting to convert to BIDS format..."
  			cd $RSCRIPTPATH
  			Rscript --vanilla $RSCRIPTPATH/BIDS_behavioral_formatter.R $filename $BIDS_DIR/"sub-"$PARTIC""/func/"$MEM_BehavioralMatch1_FILE".tsv
  			echo '\n'
  			cd $MEM_BEHAVIORAL
  		fi
  		if [[ $filename = *"match_run2"* ]] &&  [[ $filename = *".txt" ]] ; then
  			echo "found raw data for task match 2. Attempting to convert to BIDS format..."
  			cd $RSCRIPTPATH
  			Rscript --vanilla $RSCRIPTPATH/BIDS_behavioral_formatter.R $filename $BIDS_DIR/"sub-"$PARTIC""/func/"$MEM_BehavioralMatch2_FILE".tsv
  			echo '\n'
  			cd $MEM_BEHAVIORAL
  		fi
  		if [[ $filename = *"match_run3"* ]] &&  [[ $filename = *".txt" ]] ; then
  			echo "found raw data for task match 3. Attempting to convert to BIDS format..."
  			cd $RSCRIPTPATH
  			Rscript --vanilla $RSCRIPTPATH/BIDS_behavioral_formatter.R $filename $BIDS_DIR/"sub-"$PARTIC""/func/"$MEM_BehavioralMatch3_FILE".tsv
  			echo '\n'
  			cd $MEM_BEHAVIORAL
  		fi
  		if [[ $filename = *"repeat_run1"* ]] &&  [[ $filename = *".mat" ]] ; then
  			echo "found raw data for task repeat 1. Attempting to convert to BIDS format..."
  			cd $RSCRIPTPATH
  			Rscript --vanilla $RSCRIPTPATH/BIDS_behavioral_formatter.R $filename $BIDS_DIR/"sub-"$PARTIC""/func/"$MEM_BehavioralRepeat1_FILE".tsv
  			echo '\n'
  			cd $MEM_BEHAVIORAL
  		fi
  		if [[ $filename = *"repeat_run2"* ]] &&  [[ $filename = *".mat" ]] ; then
  			echo "found raw data for task repeat 2. Attempting to convert to BIDS format..."
  			cd $RSCRIPTPATH
  			Rscript --vanilla $RSCRIPTPATH/BIDS_behavioral_formatter.R $filename $BIDS_DIR/"sub-"$PARTIC""/func/"$MEM_BehavioralRepeat2_FILE".tsv
  			echo '\n'
  			cd $MEM_BEHAVIORAL
  		fi
  		if [[ $filename = *"repeat_run3"* ]] &&  [[ $filename = *".mat" ]] ; then
  			echo "found raw data for task repeat 3. Attempting to convert to BIDS format..."
  			cd $RSCRIPTPATH
  			Rscript --vanilla $RSCRIPTPATH/BIDS_behavioral_formatter.R $filename $BIDS_DIR/"sub-"$PARTIC""/func/"$MEM_BehavioralRepeat3_FILE".tsv
  			echo '\n'
  			cd $MEM_BEHAVIORAL
  		fi
	done
    

fi