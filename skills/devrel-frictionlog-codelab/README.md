
## Creation promtp

<!-- first prompt -->

```markdown
 I want to create a skill gemini-cli-custom-commands/skills/devrel-frictionlog-codelab/ with skill       
   creator. The idea is that I give you a codelab JURL like for example                                    
   https://codelabs.developers.google.com/codelabs/app-mod-workshop . Then I want you to create a folder   
   like YYYYMMDD-frictionlog-CODELAB_TITLE/ Then I want you to organize te skill so that you do the        
   following: 1. download the codelab in codelab/original/01.md, 02.m2, .. , 10.md . And copy the same     
   into codelab/proposed/ (wioth a diff with the proposed changes). Then you ask user for a GCP project id 
   with billing, or billing with no project, then you're expected to create a project for that Billing Id, 
   and start "reproducing" the codelab yourself! Apart from thebilling part, i expect the LLM to then be   
   fairly independent and start running throught the codelab like this (and the SKILL needs to give        
   reasonable directions!). It will start writing a FRICTION_LOG/01.md, ... NN.md. The idea is that we     
   tresat every page differently to help resuming if we get stuck. The folder might already exist, we get  
   stuck, we reboot the computer, and we want to take it from where wwe left it. We probably need to       
   annotate some things like PROKECT_ID and secrets in a .env and finally we want to annotate the          
   resources we're using (eg a GCE vm permalink, or cloud run isntnce,  or Cloud SQL database coordinates  
   in a mix of .env or README.md ). The big output of this whole thing is: 1. were you LLM able to run the 
   whole codelab? 2. were there inconsistencies between screenshots (if LLM if multimodal) and text and    
   your experience? The friction log markdown should track all of this experience and tag all bulletpoints 
   with "*" if its normal or with RED YELLOW GREEN bullet emojis if the experience was particularly bad,   
   good or meh. Also lets be pragmatic, if there's a typo or a wrong instruction we will use the proposed/ 
   folder to patch the markdown to a proposed solution! And use the Frction log .md to explain why that    
   needs changing.                                                                                         
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

 Also: if the codelab references an external repo, you should download the repos under external-repos/   
   (git-ignored!) and identify possibly missing or broken parts. If user is ok, you can also start filing  
   PRs to the code to fix those issues! At the end I expect a short README.md with what you did, what you  
   fojnd, a list of big mistakes and an links to all the things you fixed or suggest to fix. Keep the      
   README small, but have it link where ALL bugs are! Maybe put all the bugs as a bulletpoint list in a    
   BUGS.md

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

One last thing, I would expect a small bash or python script to setup the scaffold of the folder, and   
   mayube a tool to extract the markdown from the codelab? So we start witj a deterministic scaffold. and  
   also a .version file with "Created with skilll NAME v$VERSIOn - find me in <link to github repo of      
   url = git@github.com:palladius/gemini-cli-custom-commands.git -> hhtp >           


```

## Acceptance testing

1. Take two workshops:

1. <https://codelabs.developers.google.com/codelabs/app-mod-workshop#0>
1. <https://codelabs.developers.google.com/codelabs/build-a-simple-travel-agent-with-adk-and-gemini-cli>

Ensure the script is able to create a folder (folder should be given in ARGV[1] so we can test it with same folder over and over).
The script invocation should fail with help when invoked with no ARGV -> this ensures a --help is given and LLM picks it up with latest code - which might be more up to sdate than skill itself ;)

Ensure the scaffold is created, all pages are created (12 and 10 respectively)

Finally wait for skill me to validate a folder once you're happy with it.
THEN we can ship this skill as version `0.1.0`.
