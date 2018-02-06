#BIDS Conversion Script for UT Cognitive Neuroscience Lab's Aging Study
#accesses data from server, converts to BIDS form, and saves to server

export WORKING_DIR=/Volumes/schnyer/Aging_DecMem
export SOURCE_DIR=$WORKING_DIR/Scan_Data/Behavioral
export BIDS_DIR=$WORKING_DIR/Scan_Data/BIDS
export RSCRIPTPATH=$WORKING_DIR/Scan_Data/Behavioral

##Choose Participant
echo -en '\n'
echo "Which participant?"
read PARTIC

##Find behavioral directories
MEM_BEHAVIORAL=$SOURCE_DIR/$PARTIC/Memory
echo $MEM_BEHAVIORAL

##Create BIDS filenames
MEM_BehavioralMatch1_FILE="sub-"$PARTIC""_task-MemMatch_run_01_bold
MEM_BehavioralRepeat1_FILE="sub-"$PARTIC""_task-MemRepeat_run_01_bold
MEM_BehavioralMatch2_FILE="sub-"$PARTIC""_task-MemMatch_run_02_bold
MEM_BehavioralRepeat2_FILE="sub-"$PARTIC""_task-MemRepeat_run_02_bold
MEM_BehavioralMatch3_FILE="sub-"$PARTIC""_task-MemMatch_run_03_bold
MEM_BehavioralRepeat3_FILE="sub-"$PARTIC""_task-MemRepeat_run_03_bold

##Create BID formatted behavioral directory
if [ ! -d $BIDS_DIR/"sub-"$PARTIC""/behavioral ]; then
    mkdir -p $BIDS_DIR/"sub-"$PARTIC""/behavioral
fi

##Convert Files to BIDS Format
if [ ! -z "$MEM_BEHAVIORAL" ]; then
    for filename in "$MEM_BEHAVIORAL"/*; do
    	if [[ $filename = *"match_run1"* ]] &&  [[ $filename = *".txt" ]] ; then
  			echo "found match1"
  			cd $RSCRIPTPATH
  			Rscript --vanilla $RSCRIPTPATH/BIDS_behavioral_formatter.R $filename $BIDS_DIR/"sub-"$PARTIC""/behavioral/"$MEM_BehavioralMatch1_FILE".txt
  			cd $MEM_BEHAVIORAL
  		fi
  		if [[ $filename = *"match_run2"* ]] &&  [[ $filename = *".txt" ]] ; then
  			echo "found match 2"
  			cd $RSCRIPTPATH
  			Rscript --vanilla $RSCRIPTPATH/BIDS_behavioral_formatter.R $filename $BIDS_DIR/"sub-"$PARTIC""/behavioral/"$MEM_BehavioralMatch2_FILE".txt
  			cd $MEM_BEHAVIORAL
  		fi
  		if [[ $filename = *"match_run3"* ]] &&  [[ $filename = *".txt" ]] ; then
  			echo "found match 3"
  			cd $RSCRIPTPATH
  			Rscript --vanilla $RSCRIPTPATH/BIDS_behavioral_formatter.R $filename $BIDS_DIR/"sub-"$PARTIC""/behavioral/"$MEM_BehavioralMatch3_FILE".txt
  			cd $MEM_BEHAVIORAL
  		fi
  		if [[ $filename = *"repeat_run1"* ]] &&  [[ $filename = *".txt" ]] ; then
  			echo "found repeat 1"
  			cd $RSCRIPTPATH
  			Rscript --vanilla $RSCRIPTPATH/BIDS_behavioral_formatter.R $filename $BIDS_DIR/"sub-"$PARTIC""/behavioral/"$MEM_BehavioralRepeat1_FILE".txt
  			cd $MEM_BEHAVIORAL
  		fi
  		if [[ $filename = *"repeat_run2"* ]] &&  [[ $filename = *".txt" ]] ; then
  			echo "found repeat 2"
  			cd $RSCRIPTPATH
  			Rscript --vanilla $RSCRIPTPATH/BIDS_behavioral_formatter.R $filename $BIDS_DIR/"sub-"$PARTIC""/behavioral/"$MEM_BehavioralRepeat2_FILE".txt
  			cd $MEM_BEHAVIORAL
  		fi
  		if [[ $filename = *"repeat_run3"* ]] &&  [[ $filename = *".txt" ]] ; then
  			echo "found repeat 3"
  			cd $RSCRIPTPATH
  			Rscript --vanilla $RSCRIPTPATH/BIDS_behavioral_formatter.R $filename $BIDS_DIR/"sub-"$PARTIC""/behavioral/"$MEM_BehavioralRepeat3_FILE".txt
  			cd $MEM_BEHAVIORAL
  		fi
	done
    

fi