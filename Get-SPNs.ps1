#PowerShell script to find User SPNS (kerberoastable service accounts)

cls
$search = New-Object DirectoryServices.DirectorySearcher([ADSI]"")
$search.filter = "(servicePrincipalName=*)"

$results = $search.Findall() | ?{ $_.path -like '*CN=users*' }

foreach( $result in $results ) {
        $userEntry = $result.GetDirectoryEntry()
        Write-host "`n"
        Write-host "Object Name = "$userEntry.name -backgroundcolor "yellow" -foregroundcolor "black"
        Write-host "DN = "$userEntry.distinguishedName
        Write-host "Object Cat. = "$userEntry.objectCategory
        Write-host "servicePrincipalNames"

        $i=1
        foreach( $SPN in $userEntry.servicePrincipalName ) {
                Write-host "SPN ${i} = $SPN"
                $i+=1
        }
        Write-host ""
}
