library(tidyverse)
library(janitor)
library(readxl)

# Define the directory containing the Excel files
dir_path <- "Detention/Detention_Sheets"

# Get a list of all Excel files in the directory
file_list <- list.files(path = dir_path, pattern = "\\.xlsx$", full.names = TRUE)

# Function to read all sheets from an Excel file
read_all_sheets <- function(file) {
  target_string <- "Facilities"
  sheet_names <- excel_sheets(file)
  matching_sheets <- sheet_names[grepl(target_string, sheet_names, ignore.case = TRUE)]
  df <- lapply(matching_sheets, function(sheet) read_excel(file, sheet=sheet))[[1]]
  
  date_pattern <- "[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}"  # Matches DD-MM-YYYY or DD/MM/YYYY
  
  date <- df |>
    mutate(new = str_extract(df[[1]], date_pattern))|>
    select(new) |>
    filter(!is.na(new)) |>
    pull()
  
  row_num <- df %>%
    mutate(row_number = row_number()) %>%
    filter(.[[1]] == "Name") %>%
    pull(row_number)
  
  clean <- df |>
    row_to_names(row_number = row_num) |>
    select(1:17) |>
    rename_with(~gsub("FY[0-9]+ ALOS", "ALOS", .), everything()) |>
    mutate(`Pull Date` = date) |>
    filter(!is.na(City))
  
  return(clean)
}


# Read all Excel files and their sheets
all_data <- map(file_list, read_all_sheets)

#Combine list of dataframes
output <- bind_rows(all_data)



output_clean <- output |>
  mutate(Name = str_to_title(Name),
         City = str_to_title(City),
         Address = str_to_title(Address))|>
  mutate_at(c("Level A", "Level B", "Level C", "Level D",
              "Male Crim", "Female Crim", "Male Non-Crim", "Female Non-Crim"), 
            as.numeric)|>
  mutate(ADP = round(`Level A` + `Level B` + `Level C` + `Level D`, 2)) |>
  mutate(`Male ADP` = round(`Male Crim` + `Male Non-Crim`, 2),
         `Female ADP` = round(`Female Crim` + `Female Non-Crim`, 2))|>
  mutate(`Crim ADP`= round(`Male Crim` + `Female Crim`, 2),
         `Non_crim ADP` = round(`Male Non-Crim` + `Female Non-Crim`, 2))|>
  mutate(City = ifelse(City=="Cottonwood Fall", "Cottonwood Falls", City))|>
  mutate(City = ifelse(City == "Richwood", "Monroe", City))|>
  mutate(Name2 = case_when(Name == "Freeborn County Jail, Mn" ~ "Freeborn County Adult Detention Center",
                          Name == "Desert View Annex" ~ "Desert View",
                          Name == "Baker County Sheriff Dept." ~ "Baker County Sheriff's Office",
                          Name == "Baptist Child & Fam Svc-Staff Sec" ~ "Baptist Child & Family Services",
                          Name == "Berks County Residential Center1" ~ "Berks County Residential Center",
                          Name == "Berks County Residential Center3" ~ "Berks County Residential Center",
                          Name == "Best Western Plus El Paso Airport Hotel & Conferen" ~ "Best Western-Casa De Estrella",
                          Name == "Buffalo Service Processing Center" ~ "Buffalo (Batavia) Service Processing Center",
                          Name == "Buffalo Spc" ~ "Buffalo (Batavia) Service Processing Center",
                          Name == "Children's Village-Staff Secure" ~ "Childrens Village - Shelter",
                          Name == "Childrens Village - Tgh" ~ "Childrens Village - Shelter",
                          Name == "T Don Hutto Detention Center" ~ "T. Don Hutto Detention Center",
                          Name == "T Don Hutto Residential Center" ~ "T. Don Hutto Detention Center",
                          Name == "Tri-County Detention Center" ~ "Pulaski County Jail",
                          Name == "Orange County Jail" & State == "NY" ~ "Orange County Jail (Ny)",
                          Name == "Kay Co Justice Facility" ~ "Kay County Justice Facility",
                          Name == "Dallas County Jail - Lew Sterrett Justice Center***" ~ "Dallas County Jail - Lew Sterrett Justice Center",
                          Name == "Morrison Downtown Staff Secure" ~ "Morrison Downtown Shelter",
                          Name == "Specialized Care For Imm. Youth" ~ "Casa Heartland Guadalupe",
                          Name == "St. Clair County Jail" ~ "Saint Clair County Jail",
                          Name == "Robert A Deyton Detention Fac" ~ "Robert A Deyton Detention Facility",
                          Name == "Robert A Deyton Detention" ~ "Robert A Deyton Detention Facility",
                          Name == "Prairieland Detention Center" ~ "Prairieland Detention Facility",
                          Name == "Prairieland Suboffice Hold Room" ~ "Prairieland Detention Facility",
                          Name == "Geauga County Jail (Geaugoh)" ~ "Geauga County Jail",
                          Name == "Berks County" ~ "Berks County Secured Juvenile",
                          Name == "Tornillo-Guadalupe Poe" ~ "Tornillo Adult Hold Room",
                          Name == "Nye County Sheriff-Pahrump" ~ "Nye County Detention Center, Southern (Pahrump)",
                          Name == "Holiday Inn Expr & Stes Pho/Chndlr" ~ "Holiday Inn Express-Casa De La Luz",
                          Name == "Northwest Ice Processsing Center" ~ "Tacoma Ice Processing Center (Northwest Det Ctr)",
                          Name == "Northwest Ice Procsesing Center" ~ "Tacoma Ice Processing Center (Northwest Det Ctr)",
                          Name == "Kids Peace" ~ "Kidspeace Foster Care Program",
                          Name == "Pike County Jail" ~ "Pike County Correctional Facility",
                          Name == "Henderson Detention" ~ "Henderson Detention Center",
                          Name == "Richwood Cor Center" ~ "Richwood Correctional Center",
                          Name == "Willacy Detention Center" ~ "El Valle Detention Facility",
                          Name == "Krome Hold Room" ~ "Krome North Service Processing Center",
                          Name == "Noank Group Homes & Support Svcs" ~ "Noank Community Support Services",
                          Name == "Comfort Inn & Suites - El Paso" ~ "Comfort Suites-Casa Consuelo",
                          Name == "Jefferson County Jail***" ~ "Jefferson County Jail",
                          Name == "Deptartment Of Corrections Hagatna" ~ "Department Of Corrections Hagatna",
                          Name == "Torrance/Estancia, Nm" ~ "Torrance County Detention Facility",
                          Name == "Dodge County Jail, Juneau" ~ "Dodge County Jail",
                          Name == "Kandiyohi Co. Jail" ~ "Kandiyohi County Jail",
                          Name == "Clinton County Jail***" ~ "Clinton County Jail",
                          Name == "Plymouth Co Cor Facilty" ~ "Plymouth County Correctional Facility",
                          Name == "Otero Co Processing Center" ~ "Otero County Processing Center",
                          Name == "Strafford Co Dept Of Corr" ~ "Strafford County Corrections",
                          Name == "Port Isabel Spc" ~ "Port Isabel",
                          Name == "Orleans Parish Juvenile Facility" ~ "Orleans Parish Sheriff",
                          Name == "Comprehensive Hlth Svc-San Benito" ~ "International Edu Svcs- San Benito",
                          Name == "South Texas Fam Residential Center" ~ "South Texas Family Residential Center",
                          Name == "South Texas Family Residential Center1" ~ "South Texas Family Residential Center",
                          Name == "South Texas Family Residential Center2" ~ "South Texas Family Residential Center",
                          Name == "South Texas Family Residential Center3" ~ "South Texas Family Residential Center",
                          Name == "Trusted Adult South Tex Dilley Fsc" ~ "South Texas Family Residential Center",
                          Name == "Chase County Jail" ~ "Chase County Detention Facility",
                          Name == "Grayson County Detention Center" ~ "Grayson County Jail",
                          City == "Sault Ste Marie" ~ "Chippewa County Ssm",
                          Name == "Florence Spc" ~ "Florence Service Processing Center",
                          Name == "Folkston Annex Ipc" ~ "Annex - Folkston Ipc",
                          Name == "Northwest State Correctional Facility" ~ "Northwest State Correctional Center",
                          Name == "South Louisiana Ice Processing Center" ~ "South Louisiana Detention Center",
                          Name == "Orange County Jail" & State == "FL" ~ "Orange County Jail (Fl)",
                          Name == "St. Martin Parish Medical" ~ "St. Martin Parish Correctional Center",
                          Name == "San Luis Regional Detention Center***" ~ "San Luis Regional Detention Center",
                          Address == "409 Fm 1144" ~ "Karnes County Residential Center",
                          Name == "San Diego County Jail" ~ "George Bailey Detention Facility",
                          Name == "Coastal Bend Det. Facility" ~ "Coastal Bend Detention Facility",
                          Name == "Ica - Farmville" ~ "Immigration Centers Of America Farmville",
                          Name == "Prince Edward County (Farmville)" ~ "Immigration Centers Of America Farmville",
                          Name == "Orange County Intake Release Facility" ~ "Orange County Central Women's Jail",
                          Name == "La Palma Correction Center - Apso" ~ "La Palma Correctional Center",
                          Name == "Moshannon Valley Correctional" ~ "Moshannon Valley Processing Center",
                          Name == "South Texas Ice Processing Center1" ~ "South Texas Ice Processing Center",
                          Name == "Clinton County Corr. Fac." ~ "Clinton County Correctional Facility",
                          Name == "Clinton County Correctional" ~ "Clinton County Correctional Facility",
                          Name == "Carver County Juvenile Detention Center" ~ "Carver County Jail",
                          Name == "Clay County Justice Center" ~ "Clay County Jail",
                          Name == "Elizabeth Contract D.f." ~ "Elizabeth Contract Detention Facility",
                          Name == "Calipatria State" ~ "Cdc Calipatria Ihp",
                          Name == "Eden Detention Ctr" ~ "Eden Detention Center",
                          Name == "Southwest Key #946" ~ "Southwest Key - Browsville - Staff Secure",
                          Name == "Otay Mesa Detention Center" ~ "Otay Mesa Detention Center (San Diego Cdf)",
                          Name == "Montgomery Hold Rm" ~ "Montgomery Ice Processing Center",
                          Name == "Montgomery Processing Ctr" ~ "Montgomery Ice Processing Center",
                          Name == "Lasalle Ice Processing Center (Jena)" ~ "Central Louisiana Ice Processing Center (Clipc)",
                          Name == "Hancock Co Pub Sfty Cplx" ~ "Hancock County Public Safety Complex",
                          Name == "El Paso Spc" ~ "El Paso Service Processing Center",
                          Name == "Limestone Det Center" ~ "Limestone County Detention Center",
                          Name == "Limestone Detention Center" ~ "Limestone County Detention Center",
                          Name == "Karnes County Civil Detention Center" ~ "Karnes County Residential Center",
                          Name == "Good" ~ "Goodhue County Jail",
                          Name == "Saipan Department Of Corrections (Suspe)" ~ "Saipan Department Of Corrections (Susupe)",
                          Name == "Saipan Department Of Corr" ~ "Saipan Department Of Corrections (Susupe)",
                          .default = Name)
         )

total_final <- output_clean |>
  select(Name2, Address, City, State, Zip, `Pull Date`, ADP) |>
  distinct(Name2, `Pull Date`, .keep_all = TRUE)|>
  pivot_wider(id_cols = Name2:Zip, names_from = `Pull Date`, values_from = ADP, 
              values_fill = NA)


male <- output_clean |>
  select(Name2, Address, City, State, Zip, `Pull Date`, `Male ADP`) |>
  distinct(Name2, `Pull Date`, .keep_all = TRUE)|>
  pivot_wider(id_cols = Name2:Zip, names_from = `Pull Date`, values_from = `Male ADP`, 
              values_fill = NA)

female <- output_clean |>
  select(Name2, Address, City, State, Zip, `Pull Date`, `Female ADP`) |>
  distinct(Name2, `Pull Date`, .keep_all = TRUE)|>
  pivot_wider(id_cols = Name2:Zip, names_from = `Pull Date`, values_from = `Female ADP`, 
              values_fill = NA)

crim <- output_clean |>
  select(Name2, Address, City, State, Zip, `Pull Date`, `Crim ADP`) |>
  distinct(Name2, `Pull Date`, .keep_all = TRUE)|>
  pivot_wider(id_cols = Name2:Zip, names_from = `Pull Date`, values_from = `Crim ADP`, 
              values_fill = NA)

Non_crim <- output_clean |>
  select(Name2, Address, City, State, Zip, `Pull Date`, `Non_crim ADP`) |>
  distinct(Name2, `Pull Date`, .keep_all = TRUE)|>
  pivot_wider(id_cols = Name2:Zip, names_from = `Pull Date`, values_from = `Non_crim ADP`, 
              values_fill = NA)


names <- list("Total ADP" = total_final,
              "Female ADP" = female,
              "Male ADP" = male,
              "Criminal Status ADP" = crim,
              "Non Criminal Status ADP" = Non_crim)

write.xlsx(names, "Detention_ADP_2025-03-14.xlsx")
