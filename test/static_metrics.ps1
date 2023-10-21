function Invoke-Radon {
    <#
    .SYNOPSIS
    This function runs the radon command with different parameters on the specified paths and redirects the output to fixed output files.

    .DESCRIPTION
    The function takes in one parameter: an array of commands. It then iterates over these commands, running the radon command with each command on the specified paths and redirecting the output to a corresponding fixed output file.

    .PARAMETER Commands
    An array of strings representing the radon commands to be run.

    .EXAMPLE
    Invoke-Radon -Commands @("cc", "raw", "mi", "hal")
    #>
    param (
        [Parameter(Mandatory=$true)]
        [string[]] $Commands
    )

    $radon = "radon"
    $paths = ".\src\ .\test\ .\Launcher.py"
    $outputDir = ".\report\static"

    for ($i=0; $i -lt $Commands.length; $i++) {
        $command = $Commands[$i]
        $output = "$outputDir\$command.txt"
        Write-Host "Running radon $command..."
        & $radon $command $paths | Out-File -FilePath $output
        Write-Host "Finished running radon $command. Output saved to $output."
    }
}

Invoke-Radon -Commands @("cc", "raw", "mi", "hal")
