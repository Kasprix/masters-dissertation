

# Gametree logic
def deploy_gametree(framework, selected_argument):
  for x in framework:
    starting_argument = None
    if x.name == selected_argument:
        print("\n\nNew Section")
        print("i found it!")
        starting_argument = x
        break
    
  return starting_argument


def search_tree(framework, starting_argument):

  list_of_pairs = []

  print("Beginning argument", starting_argument.name)

  if len(starting_argument.attacked_by) > 0:
    print("\nLayer 1: ")
    for x in starting_argument.attacked_by:
      print(starting_argument.name, "is attacked by", x.name)
      # Lists pairs together to then ensure repeats don't occur
      list_of_pairs.append([x.name, starting_argument.name])

      if len(x.attacked_by) > 0:

        print("\nLayer 2:")
        for y in x.attacked_by:

          if [y.name ,x.name] not in list_of_pairs:
            print(x.name, "is attacked by", y.name)
            list_of_pairs.append([y.name, x.name])
          else: print("Duplicate")

          if len(y.attacked_by) > 0:
            print("\nLayer 3:")
            for z in y.attacked_by:
              if [z.name ,y.name] not in list_of_pairs:
                print(y.name, "is attacked by", z.name)
                #print("Layer 3, selected argument:", z.name)
                list_of_pairs.append([z.name, y.name])
              else: break

              if len(z.attacked_by) > 0:
                print("\nLayer 4:")
                for a in z.attacked_by:
                  if [a.name ,z.name] not in list_of_pairs:
                    print(z.name, "is attacked by", a.name)
                    list_of_pairs.append([a.name, z.name])
                
                if len(a.attacked_by) > 0:
                  print("\nLayer 5:")
                  # print("Layer 4, selected argument:", a.name)
                  for b in a.attacked_by:
                    if [b.name ,a.name] not in list_of_pairs:
                      print(a.name, "is attacked by", b.name)
                      list_of_pairs.append([b.name, a.name])
                else: break
          else: print("Terminate")      
  else: print("Terminate")
  print(list_of_pairs)
