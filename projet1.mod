# Data provided
/* Students list */
set ETU;
/* Establishments list */
set ETA;

/* Capacity of establishments */
param capa{i in ETA} integer, >= 0;
/* General ranking of students */
param rank_etu{i in ETU} integer, >= 1;
/* Ranking of establishments per student */
param rank_eta{i in ETU, j in ETA} integer, >= -1, < 7;

# Results researched
/* Establishment chosen per student as a list of bool */
var eta_per_etu{i in ETU, j in ETA}, binary;
/* Students chosen per establishment as a list of bool */
var etu_per_eta{i in ETA, j in ETU}, binary;

# Constraints
/* Students are present in their chosen establishment's student list */
s.t. same_choice{i in ETU, j in ETA}: eta_per_etu[i,j] == etu_per_eta[j,i];
/* No more students chosen than establishment's capacity permits */
s.t. max_capa{i in ETA}: sum{j in ETU} etu_per_eta[i, j] <= capa[i];
/* Student chosen by one and only one establishment */
s.t. one_choice1{i in ETU}: sum{j in ETA} etu_per_eta[j,i] == 1;
s.t. one_choice2{i in ETU}: sum{j in ETA} eta_per_etu[i,j] == 1;
/* Student's establishment inside student list (not ranked 0) */
s.t. in_student_list{i in ETU, j in ETA}: eta_per_etu[i,j] * rank_eta[i,j] >= 0;


# Objective
/* minimize unsatisfactory distribution */
/* max satisfaction for students */
minimize etu_choice: (sum{i in ETA, j in ETU} rank_eta[j,i]*etu_per_eta[i,j]);
/* max satisfaction for establishments */
minimize eta_choice: (sum{i in ETA, j in ETU} rank_etu[j]*etu_per_eta[i,j]);


# Resolution
solve;


# Display
printf: "Establisment attribution per student :\n\n";
for{i in ETU}{
    printf: "- %s\n", i;
    printf{j in ETA: eta_per_etu[i,j] = 1}: "\t%s", j;
    printf: "\n";
}
printf: "\n\n";
printf: "Student attribution per establishment :\n\n";
for{i in ETA}{
    printf: "- %s\n", i;
    printf{j in ETU: etu_per_eta[i,j] = 1}: "\t%s", j;
    printf: "\n";
}

end;
