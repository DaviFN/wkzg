from wkzg_common import *

cpp_source_file_extensions = ['.cpp', '.cxx', '.cc']
cpp_header_file_extensions = ['.hh', '.hpp', '.h']

def find_position_of_final_bracket(string: str):
    nNestedBraces = 0 # when this gets to 0 then it is the final bracket of the class
    consideredInitialBracketAlready = False

    nCharactersToAdvance = 0
    for character in string:
        if character == '{':
            nNestedBraces = nNestedBraces + 1
            consideredInitialBracketAlready = True
        elif character == '}':
            nNestedBraces = nNestedBraces - 1
        if nNestedBraces == 0 and consideredInitialBracketAlready:
            break
        nCharactersToAdvance = nCharactersToAdvance + 1

    if nNestedBraces != 0 or not consideredInitialBracketAlready:
        return -1
    
    return nCharactersToAdvance

def find_position_of_final_bracket_of_class_declaration(fileContent: str, className: str):
    positionOfClassDeclaration = fileContent.find('class ' + className)
    if positionOfClassDeclaration == -1:
        return -1
    
    restOfFileContent = fileContent[positionOfClassDeclaration:]

    positionOfInitialBracket = restOfFileContent.find('{')
    if positionOfClassDeclaration == -1:
        return -1
    
    restOfFileContent = restOfFileContent[positionOfInitialBracket:]

    positionOfFinalBracket = find_position_of_final_bracket(restOfFileContent)
    if positionOfFinalBracket == -1:
        return -1
    
    restOfFileContent = restOfFileContent[positionOfFinalBracket:]

    return fileContent.find(restOfFileContent)

def find_position_of_first_constructor_of_class(fileContent: str, className: str):
    positionOfFirstConstructorOfClass = fileContent.find(className + '::' + className)
    return positionOfFirstConstructorOfClass

def find_positions_of_last_brackets_of_class_constructors(fileContent: str, className: str):
    positionsOfLastBracketsOfClassConstructors = []
    
    modifiedFileContent = fileContent

    while True:
        positionOfConstructorOfClass = modifiedFileContent.find(className + '::' + className)

        if positionOfConstructorOfClass == -1:
            break
        
        modifiedFileContent = modifiedFileContent[positionOfConstructorOfClass:]

        positionOfBracket = modifiedFileContent.find('{')
        if positionOfBracket == -1:
            break
        
        modifiedFileContent = modifiedFileContent[positionOfBracket:]

        positionOfFinalBracket = find_position_of_final_bracket(modifiedFileContent)

        if positionOfFinalBracket == -1:
            break

        modifiedFileContent = modifiedFileContent[positionOfFinalBracket:]

        positionsOfSuchLastBracketsGivenOriginalFileContent = fileContent.find(modifiedFileContent)
        positionsOfLastBracketsOfClassConstructors.append(positionsOfSuchLastBracketsGivenOriginalFileContent)

    return positionsOfLastBracketsOfClassConstructors

def apply_wkzg_for_cpp_source_file(file: str, classNames):
    print('applying wkzg for C++ source file: ' + file)

    fileContent = get_file_content(file)

    for className in classNames:
        positionOfFirstConstructor = find_position_of_first_constructor_of_class(fileContent, className)

        if positionOfFirstConstructor != -1:

            contentToInsert = 'void ' + className + '::onConstructorCalled()\n{\n\tinstanceId = counter;\n\t++counter;\n}\nint ' + className + '::counter = 0;\n'

            fileContent = insert_str(fileContent, contentToInsert, positionOfFirstConstructor)
        
    positionsOfLastBracketsOfClassConstructors = find_positions_of_last_brackets_of_class_constructors(fileContent, className)

    print('positionsOfLastBracketsOfClassConstructors has ' + str(len(positionsOfLastBracketsOfClassConstructors)))

    nPositions = len(positionsOfLastBracketsOfClassConstructors)
    currentPosition = 0
    for positionOfLastBracketsOfClassConstructors in positionsOfLastBracketsOfClassConstructors:

        contentToInsert = '\n\tonConstructorCalled();\n'

        fileContent = insert_str(fileContent, contentToInsert, positionOfLastBracketsOfClassConstructors)
        
        #adjusting the remaining positions, since we just inserted something
        for i in range(currentPosition, nPositions):
            positionsOfLastBracketsOfClassConstructors[i] = positionsOfLastBracketsOfClassConstructors[i] + len(contentToInsert)

        ++currentPosition

    save_file_content(file, fileContent)

def apply_wkzg_for_cpp_header_file(file: str, classNames):
    print('applying wkzg for C++ header file: ' + file)

    fileContent = get_file_content(file)

    for className in classNames:
        positionOfFinalBracketOfClass = find_position_of_final_bracket_of_class_declaration(fileContent, className)

        if positionOfFinalBracketOfClass != -1:
            contentToInsert = '\npublic:\n\tvoid onConstructorCalled();\n\tstatic int counter;\n\tint instanceId = 0;\n'

            fileContent = insert_str(fileContent, contentToInsert, positionOfFinalBracketOfClass)

            save_file_content(file, fileContent)


def apply_wkzg(file: str, classNames):
    print('applying wkzg for file: ' + file)

    extension = get_file_extension(file)
    print('file extension:' + extension)

    if(extension in cpp_source_file_extensions):
        apply_wkzg_for_cpp_source_file(file, classNames)
    if(extension in cpp_header_file_extensions):
        apply_wkzg_for_cpp_header_file(file, classNames)