from arrow_string import *
from parseResult import ParseResult
from parser_ import *
from constants import *
from nodes import *
from error import *
from lexar import *
from rt_result import *
from values import *
from number import *
from interpreter import *
from baseFunction import *
from context import Context
from symbols import SymbolTable
import os

import math


Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)

class BuiltInFunction(BaseFunction):
  def __init__(self, name):
    super().__init__(name)

  def execute(self, args):
    res = RTResult()
    exec_ctx = self.generate_new_context()

    method_name = f'execute_{self.name}'
    method = getattr(self, method_name, self.no_visit_method)

    res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
    if res.should_return(): return res

    return_value = res.register(method(exec_ctx))
    if res.should_return(): return res
    return res.success(return_value)
  
  def no_visit_method(self, node, context):
    raise Exception(f'No execute_{self.name} method defined')

  def copy(self):
    copy = BuiltInFunction(self.name)
    copy.set_context(self.context)
    copy.set_pos(self.pos_start, self.pos_end)
    return copy

  def __repr__(self):
    return f"<{constants.get("built-in")} {self.name}>"

  #####################################

  def execute_xaffa(self, exec_ctx):
    print(str(exec_ctx.symbol_table.get('value')))
    return RTResult().success(Number.null)
  execute_xaffa.arg_names = ['value']
  
  def execute_xaffaa(self, exec_ctx):
    return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))
  execute_xaffaa.arg_names = ['value']
  
  def execute_gelso(self, exec_ctx):
    text = input()
    return RTResult().success(String(text))
  execute_gelso.arg_names = []

  def execute_gelsoInt(self, exec_ctx):
    while True:
      text = input()
      try:
        number = int(text)
        break
      except ValueError:
        print(f"'{text}' {constants.get("must-be-int")}")
    return RTResult().success(Number(number))
  execute_gelsoInt.arg_names = []

  def execute_dhayiso(self, exec_ctx):
    os.system('clear' if os.name == 'nt' else 'cls') 
    return RTResult().success(Number.null)
  execute_dhayiso.arg_names = []

  def execute_is_number(self, exec_ctx):
    is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
    return RTResult().success(Number.true if is_number else Number.false)
  execute_is_number.arg_names = ["value"]

  def execute_is_string(self, exec_ctx):
    is_number = isinstance(exec_ctx.symbol_table.get("value"), String)
    return RTResult().success(Number.true if is_number else Number.false)
  execute_is_string.arg_names = ["value"]

  def execute_is_list(self, exec_ctx):
    is_number = isinstance(exec_ctx.symbol_table.get("value"), List)
    return RTResult().success(Number.true if is_number else Number.false)
  execute_is_list.arg_names = ["value"]

  def execute_is_function(self, exec_ctx):
    is_number = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
    return RTResult().success(Number.true if is_number else Number.false)
  execute_is_function.arg_names = ["value"]

  def execute_guja(self, exec_ctx):
    list_ = exec_ctx.symbol_table.get("list")
    value = exec_ctx.symbol_table.get("value")

    if not isinstance(list_, List):
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        "First argument must be list",
        exec_ctx
      ))

    list_.elements.append(value)
    return RTResult().success(Number.null)
  execute_guja.arg_names = ["list", "value"]

  def execute_kessa(self, exec_ctx):
    list_ = exec_ctx.symbol_table.get("list")
    index = exec_ctx.symbol_table.get("index")

    if not isinstance(list_, List):
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        "First argument must be list",
        exec_ctx
      ))

    if not isinstance(index, Number):
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        "Second argument must be number",
        exec_ctx
      ))

    try:
      element = list_.elements.pop(index.value)
    except:
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        'Element at this index could not be removed from list because index is out of bounds',
        exec_ctx
      ))
    return RTResult().success(element)
  execute_kessa.arg_names = ["list", "index"]

  def execute_walakiso(self, exec_ctx):
    listA = exec_ctx.symbol_table.get("listA")
    listB = exec_ctx.symbol_table.get("listB")

    if not isinstance(listA, List):
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        "First argument must be list",
        exec_ctx
      ))

    if not isinstance(listB, List):
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        "Second argument must be list",
        exec_ctx
      ))

    listA.elements.extend(listB.elements)
    return RTResult().success(Number.null)
  execute_walakiso.arg_names = ["listA", "listB"]

  def execute_adusse(self, exec_ctx):
    list_ = exec_ctx.symbol_table.get("list")

    if not isinstance(list_, List):
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        "Argument must be list",
        exec_ctx
      ))

    return RTResult().success(Number(len(list_.elements)))
  execute_adusse.arg_names = ["list"]

  def execute_run(self, exec_ctx):
    fn = exec_ctx.symbol_table.get("fn")

    if not isinstance(fn, String):
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        "Second argument must be string",
        exec_ctx
      ))

    fn = fn.value

    try:
      with open(fn, "r") as f:
        script = f.read()
    except Exception as e:
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        f"Failed to load script \"{fn}\"\n" + str(e),
        exec_ctx
      ))

    _, error = run(fn, script)
    
    if error:
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        f"Failed to finish executing script \"{fn}\"\n" +
        error.as_string(),
        exec_ctx
      ))

    return RTResult().success(Number.null)
  execute_run.arg_names = ["fn"]


BuiltInFunction.xaffa       = BuiltInFunction("xaffa")
BuiltInFunction.xaffaa      = BuiltInFunction("xaffaa")
BuiltInFunction.gelso       = BuiltInFunction("gelso")
BuiltInFunction.gelsoInt    = BuiltInFunction("gelsoInt")
BuiltInFunction.dhayiso     = BuiltInFunction("dhayiso")
BuiltInFunction.is_number   = BuiltInFunction("is_number")
BuiltInFunction.is_string   = BuiltInFunction("is_string")
BuiltInFunction.is_list     = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.guja        = BuiltInFunction("guja")
BuiltInFunction.kessa       = BuiltInFunction("kessa")
BuiltInFunction.walakiso    = BuiltInFunction("walakiso")
BuiltInFunction.adusse		  = BuiltInFunction("adusse")
BuiltInFunction.run					= BuiltInFunction("run")


global_symbol_table = SymbolTable()
global_symbol_table.set("ayikoka", Number.null)
global_symbol_table.set("worddo", Number.false)
global_symbol_table.set("tuma", Number.true)
global_symbol_table.set("hisabe_pi", Number.math_PI)
global_symbol_table.set("xaffa", BuiltInFunction.xaffa)
global_symbol_table.set("xaffaa", BuiltInFunction.xaffaa)
global_symbol_table.set("gelso", BuiltInFunction.gelso)
global_symbol_table.set("gelsoInt", BuiltInFunction.gelsoInt)
global_symbol_table.set("dhayiso", BuiltInFunction.dhayiso)
global_symbol_table.set("IS_NUM", BuiltInFunction.is_number)
global_symbol_table.set("IS_STR", BuiltInFunction.is_string)
global_symbol_table.set("IS_LIST", BuiltInFunction.is_list)
global_symbol_table.set("IS_FUN", BuiltInFunction.is_function)
global_symbol_table.set("guja", BuiltInFunction.guja)
global_symbol_table.set("kessa", BuiltInFunction.kessa)
global_symbol_table.set("walakiso", BuiltInFunction.walakiso)
global_symbol_table.set("adusse", BuiltInFunction.adusse)
global_symbol_table.set("run", BuiltInFunction.run)

def run(fn, text):
  # Generate tokens
  lexer = Lexer(fn, text)
  tokens, error = lexer.make_tokens()
  if error: return None, error
  
  # Generate AST
  parser = Parser(tokens)
  ast = parser.parse()
  if ast.error: return None, ast.error

  # Run program
  interpreter = Interpreter()
  context = Context('<program>')
  context.symbol_table = global_symbol_table
  result = interpreter.visit(ast.node, context)

  return result.value, result.error